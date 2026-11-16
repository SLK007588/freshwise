
import streamlit as st
import pandas as pd
from datetime import date, timedelta

RECIPES = [
    {
        "name": "Spinach & Tomato Pasta",
        "ingredients": ["spinach", "tomatoes", "pasta"],
        "instructions": "Cook the pasta. Sauté the tomatoes and spinach, then combine.",
    },
    {
        "name": "Vegetable Omelette",
        "ingredients": ["eggs", "spinach", "tomatoes"],
        "instructions": "Beat the eggs, add chopped vegetables, and cook in a pan.",
    },
    {
        "name": "Tomato Pasta",
        "ingredients": ["tomatoes", "pasta"],
        "instructions": "Cook the pasta and combine with sautéed tomatoes.",
    },
    {
        "name": "Banana Smoothie",
        "ingredients": ["banana", "milk"],
        "instructions": "Blend the banana and milk until smooth.",
    },
    {
        "name": "Egg Sandwich",
        "ingredients": ["eggs", "bread"],
        "instructions": "Cook the eggs and serve between slices of bread.",
    },
]

st.set_page_config(
    page_title="FreshWise",
    page_icon="🥬",
    layout="wide"
)

st.title("🥬 FreshWise")
st.caption("Understand Your Food. Reduce Your Waste.")

# Sample data, kept during the current Streamlit session
if "pantry" not in st.session_state:
    st.session_state.pantry = [
        {"name": "Spinach", "expiry": date.today() + timedelta(days=1)},
        {"name": "Milk", "expiry": date.today() + timedelta(days=3)},
        {"name": "Eggs", "expiry": date.today() + timedelta(days=7)},
        {"name": "Tomatoes", "expiry": date.today() - timedelta(days=1)}
    ]

def freshness_status(expiry):
    days = (expiry - date.today()).days
    if days < 0:
        return "Past entered date"
    if days <= 2:
        return "Use soon"
    return "Not flagged"


def recommend_recipes(pantry):
    """Rank catalogue recipes by pantry overlap and use-soon ingredients."""
    available = {}
    for item in pantry:
        available.setdefault(item["name"].strip().casefold(), []).append(item)

    recommendations = []
    for recipe in RECIPES:
        matched = [ingredient for ingredient in recipe["ingredients"] if ingredient in available]
        if not matched:
            continue
        missing = [ingredient for ingredient in recipe["ingredients"] if ingredient not in available]
        urgent = [
            ingredient for ingredient in matched
            if any(freshness_status(item["expiry"]) == "Use soon" for item in available[ingredient])
        ]
        score = len(matched) * 10 + len(urgent) * 5 - len(missing) * 2
        reasons = [f"uses {len(matched)} ingredient(s) already in your pantry"]
        if urgent:
            reasons.append("prioritises items flagged Use soon: " + ", ".join(urgent))
        if missing:
            reasons.append("still needs: " + ", ".join(missing))
        else:
            reasons.append("all listed ingredients are in your pantry")
        recommendations.append({
            **recipe,
            "matched": matched,
            "missing": missing,
            "urgent": urgent,
            "score": score,
            "reason": "; ".join(reasons),
        })
    return sorted(recommendations, key=lambda item: (-item["score"], item["name"]))

st.subheader("Pantry Overview")

total = len(st.session_state.pantry)
soon = sum(
    freshness_status(item["expiry"]) == "Use soon"
    for item in st.session_state.pantry
)
past = sum(
    freshness_status(item["expiry"]) == "Past entered date"
    for item in st.session_state.pantry
)

c1, c2, c3 = st.columns(3)
c1.metric("Total Items", total)
c2.metric("Use Soon", soon)
c3.metric("Past Entered Date", past)

st.subheader("Your Pantry")

if st.session_state.pantry:
    rows = [
        {
            "Food": item["name"],
            "Entered Date": item["expiry"].isoformat(),
            "Status": freshness_status(item["expiry"])
        }
        for item in st.session_state.pantry
    ]
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
else:
    st.info("Your pantry is empty. Add an item below.")

if st.session_state.pantry:
    with st.expander("Correct pantry details"):
        edit_choices = {
            f"{i + 1}. {item['name']} ({item['expiry']})": i
            for i, item in enumerate(st.session_state.pantry)
        }
        edit_label = st.selectbox("Choose an item to correct", list(edit_choices), key="edit_item_choice")
        edit_index = edit_choices[edit_label]
        with st.form("edit_item"):
            corrected_name = st.text_input("Food name", value=st.session_state.pantry[edit_index]["name"])
            corrected_expiry = st.date_input(
                "Use-by / best-before / estimated date",
                value=st.session_state.pantry[edit_index]["expiry"],
            )
            if st.form_submit_button("Save correction"):
                if corrected_name.strip():
                    st.session_state.pantry[edit_index] = {
                        "name": corrected_name.strip(),
                        "expiry": corrected_expiry,
                    }
                    st.rerun()
                else:
                    st.error("Please enter a food name.")

st.subheader("Recipe Recommendations")
st.caption("Suggestions are selected from a small, predefined recipe list using transparent rules.")
show_explanations = st.toggle("Show why each recipe was suggested", value=True)
recommendations = recommend_recipes(st.session_state.pantry)
if "dismissed_recipes" not in st.session_state:
    st.session_state.dismissed_recipes = set()

visible_recommendations = [
    item for item in recommendations if item["name"] not in st.session_state.dismissed_recipes
]
if visible_recommendations:
    for recipe in visible_recommendations:
        with st.container(border=True):
            st.markdown(f"#### {recipe['name']}")
            st.write(recipe["instructions"])
            st.caption(
                "In pantry: " + (", ".join(recipe["matched"]) or "none")
                + " · Missing: " + (", ".join(recipe["missing"]) or "none")
            )
            if show_explanations:
                st.info("Why this recipe? " + recipe["reason"])
            if st.button("Dismiss suggestion", key=f"dismiss_{recipe['name']}"):
                st.session_state.dismissed_recipes.add(recipe["name"])
                st.rerun()
else:
    st.info("No recipe suggestions yet. Add or correct pantry items that match a listed recipe.")

st.subheader("Add Grocery")

with st.form("add_item", clear_on_submit=True):
    name = st.text_input("Food name")
    expiry = st.date_input(
        "Use-by / best-before / estimated date",
        value=date.today() + timedelta(days=3)
    )
    submitted = st.form_submit_button("Add to Pantry")

    if submitted:
        if name.strip():
            st.session_state.pantry.append({
                "name": name.strip(),
                "expiry": expiry
            })
            st.rerun()
        else:
            st.error("Please enter a food name.")

st.subheader("Remove Grocery")

if st.session_state.pantry:
    choices = {
        f"{i + 1}. {item['name']} ({item['expiry']})": i
        for i, item in enumerate(st.session_state.pantry)
    }
    selected = st.selectbox("Select an item", list(choices.keys()))

    if st.button("Remove Selected Item"):
        index = choices[selected]
        st.session_state.pantry.pop(index)
        st.rerun()

st.divider()
st.info(
    "Prototype only: freshness flags and recipe rankings use entered dates and simple rules; "
    "the recipes come from a fixed example catalogue. These features do not establish whether "
    "food is safe to eat. Pantry changes are kept only for the current session."
)
