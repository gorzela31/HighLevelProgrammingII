import streamlit as st
import random
from src.models import Recipe
from src.services.recipe_service import get_recipe_service

st.set_page_config(page_title="Przepiśnik", page_icon="🍲", layout="wide")

# CSS dla bardziej kompaktowych list bullet point
st.markdown(
    """
    <style>
    ul {
        margin-top: 0;
        margin-bottom: 0;
        padding-left: 1.2em;
    }
    ul li {
        margin-bottom: 0;
        line-height: 1.2;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

service = get_recipe_service(db_path="przepisnik.db")


def _safe_rerun():
    """Bezpiecznie odświeża aplikację."""
    try:
        if hasattr(st, "rerun"):
            st.rerun()
        else:
            st.experimental_rerun()
    except Exception:
        pass


st.sidebar.title("Przepiśnik")
page = st.sidebar.radio(
    "Nawigacja",
    [
        "Dashboard",
        "Dodaj przepis",
        "Przeglądaj przepisy",
        "Ulubione",
        "O aplikacji"
    ],
)


def recipe_card(r: Recipe):
    """Renderuje kartę pojedynczego przepisu wraz z akcjami."""
    with st.container():
        st.subheader(r.title)
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        with col1:
            st.caption(
                f"Czas przygotowania: {r.prep_time_minutes} min"
                if r.prep_time_minutes
                else "Czas przygotowania: brak danych"
            )
        with col2:
            if st.button(
                (
                    "★ Usuń z ulubionych"
                    if r.favorite
                    else "☆ Dodaj do ulubionych"
                ),
                key=f"fav_{r.id}",
            ):
                service.set_favorite(r.id, not r.favorite)
                _safe_rerun()
        with col3:
            if st.button("Edytuj", key=f"edit_btn_{r.id}"):
                st.session_state[f"editing_{r.id}"] = not st.session_state.get(
                    f"editing_{r.id}", False
                )
        with col4:
            if st.button("Usuń", key=f"del_{r.id}"):
                service.delete(r.id)
                st.success(f"Usunięto przepis: {r.title}")
                _safe_rerun()

        # Formularz edycji pod kartą
        if st.session_state.get(f"editing_{r.id}", False):
            with st.form(f"edit_form_{r.id}"):
                new_title = st.text_input("Tytuł", value=r.title)
                new_prep_time = st.number_input(
                    "Czas przygotowania [min]",
                    min_value=0,
                    step=5,
                    value=r.prep_time_minutes,
                )
                new_tags = st.text_input("Tagi", value=r.tags)
                new_fav = st.checkbox("Ulubiony", value=r.favorite)
                new_ingredients = st.text_area(
                    "Składniki", value=r.ingredients, height=150
                )
                new_instructions = st.text_area(
                    "Instrukcje", value=r.instructions, height=200
                )
                submitted = st.form_submit_button("Zapisz zmiany")
                if submitted:
                    try:
                        updated = Recipe(
                            id=r.id,
                            title=new_title,
                            ingredients=new_ingredients,
                            instructions=new_instructions,
                            prep_time_minutes=int(new_prep_time),
                            tags=new_tags,
                            favorite=new_fav,
                            created_at=r.created_at,
                        )
                        service.update(updated)
                        st.success("Zaktualizowano przepis.")
                        st.session_state[f"editing_{r.id}"] = False
                        _safe_rerun()
                    except ValueError as e:
                        st.error(str(e))

        with st.expander("Składniki"):
            if r.ingredients:
                for line in r.ingredients.splitlines():
                    clean = line.strip()
                    if clean:
                        st.markdown(f"- {clean}")
            else:
                st.write("_brak_")

        with st.expander("Instrukcje"):
            st.write(r.instructions or "_brak_")

        if r.tags:
            st.caption("Tagi: " + r.tags)


# --- Dashboard ---
if page == "Dashboard":
    st.title("Przepiśnik")
    c1, c2, c3 = st.columns(3)
    c1.metric("Liczba przepisów", service.count())
    c2.metric("Ulubione", service.count_favorites())
    avg = service.avg_prep_time()
    c3.metric("Średni czas", f"{avg:.0f} min" if avg else "brak")

    st.markdown("---")
    st.subheader("Losowy przepis dnia")
    all_recipes = service.list_all()
    if not all_recipes:
        st.info(
            "Brak przepisów w bazie. Dodaj coś w zakładce 'Dodaj przepis'."
        )
    else:
        if st.button("Wylosuj przepis"):
            st.session_state["random_recipe"] = random.choice(all_recipes)
            _safe_rerun()

        random_recipe = st.session_state.get("random_recipe")
        if random_recipe:
            st.success(f"Wybrano: **{random_recipe.title}**")
            with st.expander("Składniki"):
                if random_recipe.ingredients:
                    for line in random_recipe.ingredients.splitlines():
                        clean = line.strip()
                        if clean:
                            st.markdown(f"- {clean}")
                else:
                    st.write("_brak_")
            with st.expander("Instrukcje"):
                st.write(random_recipe.instructions or "_brak_")
            st.caption(
                f"Czas: {random_recipe.prep_time_minutes} min | "
                f"Tagi: {random_recipe.tags or 'brak'}"
            )

# --- Dodaj przepis ---
elif page == "Dodaj przepis":
    st.title("Dodaj przepis")
    title = st.text_input("Tytuł")
    colA, colB = st.columns([1, 1])
    with colA:
        prep_time = st.number_input(
            "Czas przygotowania [min]",
            min_value=0,
            step=5
        )
        tags = st.text_input("Tagi", placeholder="np. wege, bezglutenowe")
    with colB:
        fav = st.checkbox("Ulubiony", value=False)
    ingredients = st.text_area("Składniki", height=180)
    instructions = st.text_area("Instrukcje", height=220)
    if st.button("Zapisz przepis"):
        try:
            recipe = Recipe.new(
                title=title,
                ingredients=ingredients,
                instructions=instructions,
                prep_time_minutes=int(prep_time),
                tags=tags,
                favorite=fav,
            )
            rid = service.add(recipe)
            st.success(f"Zapisano przepis #{rid}")
            _safe_rerun()
        except ValueError as e:
            st.error(str(e))

# --- Przeglądaj przepisy ---
elif page == "Przeglądaj przepisy":
    st.title("Przepisy")
    with st.expander("Filtry"):
        fcol1, fcol2, fcol3, fcol4 = st.columns([2, 1, 1, 1])
        with fcol1:
            q = st.text_input(
                "Szukaj po tytule, składnikach lub tagach",
                key="q"
            )
        with fcol2:
            max_time = st.number_input(
                "Maksymalny czas [min]", min_value=0, step=5, value=0
            )
        with fcol3:
            only_fav = st.checkbox("Tylko ulubione", value=False)
        with fcol4:
            tags = service.list_tags()
            tag_options = ["(bez filtra)"] + tags
            tag_filter = st.selectbox("Tag", tag_options, index=0)
        if st.button("Zastosuj filtry"):
            _safe_rerun()

    results = service.search(
        q=st.session_state.get("q", ""),
        max_time=(max_time if max_time > 0 else None),
        only_fav=only_fav,
        tag=(None if tag_filter == "(bez filtra)" else tag_filter),
    )
    if not results:
        st.info("Brak wyników")
    else:
        for r in results:
            recipe_card(r)

# --- Ulubione ---
elif page == "Ulubione":
    st.title("Ulubione przepisy")
    favs = service.list_favorites()
    if not favs:
        st.info("Brak ulubionych")
    else:
        for r in favs:
            recipe_card(r)

# --- O aplikacji ---
elif page == "O aplikacji":
    st.title("O aplikacji")
    st.write(
        """
        Przepiśnik to prosta i wygodna
        aplikacja do przechowywania i przeglądania przepisów kulinarnych.
        Możesz w niej dodawać swoje ulubione przepisy,
        zapisywać składniki, instrukcje i czas przygotowania,
        a także oznaczać wybrane potrawy jako ulubione,
        aby mieć do nich szybki dostęp.
        W każdej chwili możesz edytować lub usuwać przepisy,
        filtrować je po tagach i czasie przygotowania,
        a także skorzystać z przycisku losowania,
        który podpowie Ci, co ugotować dziś.
        Przepiśnik sprawdzi się jako
        Twoja osobista książka kucharska dostępna zawsze pod ręką.
        """
    )
