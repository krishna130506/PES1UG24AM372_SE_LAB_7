"""Hypothesis property-based tests for elevator_dispatch."""
import pytest
from hypothesis import given, strategies as st
from elevator_dispatch import parse_request, total_travel, load_percent


@given(st.integers(min_value=0, max_value=10**6), st.integers(min_value=0, max_value=10**6))
def test_parse_request_round_trip(start, end):
    assert parse_request(f"{start}->{end}") == (start, end)


@given(st.lists(st.integers(min_value=0, max_value=10**5), min_size=1, max_size=30))
def test_total_travel_matches_reference(floors):
    text = ",".join(map(str, floors))
    expected = sum(abs(floors[i + 1] - floors[i]) for i in range(len(floors) - 1))
    assert total_travel(text) == expected


@given(st.integers(min_value=0, max_value=10**6), st.integers(min_value=1, max_value=10**6))
def test_load_percent_matches_reference(load, capacity):
    load = min(load, capacity)
    assert load_percent(f"{load} of {capacity}") == load * 100 // capacity


@given(st.one_of(st.none(), st.integers(), st.text()))
def test_parse_request_malformed_values_are_rejected(value):
    if isinstance(value, str) and value.count("->") == 1:
        left, right = (part.strip() for part in value.split("->"))
        if left.lstrip("+-").isdigit() and right.lstrip("+-").isdigit() and int(left) >= 0 and int(right) >= 0:
            return
    with pytest.raises(ValueError):
        parse_request(value)


@given(st.one_of(st.none(), st.integers(), st.text()))
def test_total_travel_malformed_values_are_rejected(value):
    if isinstance(value, str) and value.strip():
        parts = [part.strip() for part in value.split(",")]
        if all(p.lstrip("+-").isdigit() and int(p) >= 0 for p in parts):
            return
    with pytest.raises(ValueError):
        total_travel(value)


@given(st.one_of(st.none(), st.integers(), st.text()))
def test_load_percent_malformed_values_are_rejected(value):
    if isinstance(value, str) and value.count(" of ") == 1:
        left, right = (part.strip() for part in value.split(" of "))
        if left.lstrip("+-").isdigit() and right.lstrip("+-").isdigit():
            load, capacity = int(left), int(right)
            if 0 <= load <= capacity and capacity > 0:
                return
    with pytest.raises(ValueError):
        load_percent(value)


@pytest.mark.parametrize("value", ["5->", "->9", "5->9->10", "-1->4", "a->4"])
def test_parse_request_rejects_invalid_examples(value):
    with pytest.raises(ValueError):
        parse_request(value)


@pytest.mark.parametrize("value", ["", "1,,3", "1,a,3", "-1,2"])
def test_total_travel_rejects_invalid_examples(value):
    with pytest.raises(ValueError):
        total_travel(value)


@pytest.mark.parametrize("value", ["450 of 0", "-1 of 10", "11 of 10", "x of 10", "10/20"])
def test_load_percent_rejects_invalid_examples(value):
    with pytest.raises(ValueError):
        load_percent(value)
