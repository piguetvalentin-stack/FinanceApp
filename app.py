import streamlit as st
import pandas as pd
import plotly.express as px

from database import (
    create_database,
    add_expense,
    get_expenses,
    delete_expense,
    get_savings_goals,
    add_savings_goal,
    delete_savings_goal,
    update_savings_goal_amount,
    update_expense,
    add_recurring_expense,
    get_recurring_expenses,
    add_or_update_category,
    get_categories,
    delete_category
)

st.set_page_config(
    page_title="Finance Familiale",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Finance Familiale")
create_database()

budgets = {
    "Courses": 800,
    "Essence": 250,
    "Restaurant": 200,
    "Maison": 500,
    "Loisirs": 200,
    "Santé": 150,
    "Autre": 200

    
}
objectifs = {
    "💍 Mariage": {
        "actuel": 0,
        "objectif": 20000
    },
    "📈 ETF World": {
        "actuel": 0,
        "objectif": 50000
    },
    "🏖 Vacances": {
        "actuel": 0,
        "objectif": 5000
    },
    "🛡 Fonds de sécurité": {
        "actuel": 0,
        "objectif": 15000
    }
}

expenses = get_expenses()

categories_from_db = get_categories()

if categories_from_db:
    categories_list = [category[0] for category in categories_from_db]
    budgets = {category[0]: category[1] for category in categories_from_db}
else:
    categories_list = ["Courses", "Essence", "Restaurant", "Maison", "Loisirs", "Santé", "Autre"]
months = ["Tous"]

if expenses:
    months.extend(
        sorted(
            list(set(expense[1][:7] for expense in expenses)),
            reverse=True
        )
    )

selected_month = st.selectbox("Mois à afficher", months)

df = pd.DataFrame(
    expenses,
    columns=[
        "ID",
        "Date",
        "Catégorie",
        "Montant (€)",
        "Description",
        "Payeur",
        "Carte"
    ]
) if expenses else pd.DataFrame(
    columns=[
        "ID",
        "Date",
        "Catégorie",
        "Montant (€)",
        "Description",
        "Payeur",
        "Carte"
    ]
)

if selected_month != "Tous" and not df.empty:
    df = df[df["Date"].str.startswith(selected_month)]

tab_add, tab_dashboard, tab_savings, tab_recurring, tab_settings, tab_history = st.tabs(
    [
        "➕ Ajouter",
        "📊 Dashboard",
        "🎯 Épargne",
        "🔁 Récurrentes",
        "⚙️ Paramètres",
        "📋 Historique"
    ]
)

with tab_add:
    st.header("Ajouter une dépense")

    with st.form("form_ajout_depense"):
        date = st.date_input("Date")
        montant = st.number_input("Montant (€)", min_value=0.0, step=0.01)

        st.write("Catégorie")

        categories = [
            "🛒 Courses",
            "⛽ Essence",
            "🍔 Restaurant",
            "🏠 Maison",
            "🎮Loisirs",
            "🏥 Santé",
            "📦 Autre"
        ]

        categorie = st.radio(
            "Choisis une catégorie",
            categories,
            horizontal=True,
            label_visibility="collapsed"
        )

        categorie = categorie.split(" ", 1)[1]

        st.write("Qui a payé ?")

        payeurs = [
            "👨 Valentin",
            "👩 Julia",
            "🏠 Commun"
        ]

        payeur = st.radio(
        "Choisis le payeur",
        payeurs,
        horizontal=True,
        label_visibility="collapsed"
        )

        payeur = payeur.split(" ", 1)[1]

        st.write("Mode de paiement")

        cartes = [
            "💳 Crédit Mutuel",
            "📈 Trade Republic",
            "💵 Cash"
        ]

        carte = st.radio(
            "Choisis le mode de paiement",
            cartes,
            horizontal=True,
            label_visibility="collapsed"
        )

        carte = carte.split(" ", 1)[1]

        description = st.text_input("Description")

        submitted = st.form_submit_button("Ajouter la dépense")

        if submitted:
            add_expense(str(date), montant, categorie, description, payeur, carte)
            st.success("Dépense enregistrée !")
            st.balloons()

with tab_dashboard:
    st.header("Dashboard")

    if df.empty:
        st.info("Aucune dépense à afficher pour cette période.")
    else:
        total_depenses = df["Montant (€)"].sum()
        nombre_depenses = len(df)
        moyenne_depense = total_depenses / nombre_depenses if nombre_depenses > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Total période", f"{total_depenses:.2f} €")
        col2.metric("🧾 Nombre", nombre_depenses)
        col3.metric("📊 Moyenne", f"{moyenne_depense:.2f} €")

        st.subheader("Dépenses par payeur")

        df_payeurs = df.groupby("Payeur")["Montant (€)"].sum().reset_index()
        cols_payeurs = st.columns(len(df_payeurs))

        for index, row in df_payeurs.iterrows():
            cols_payeurs[index].metric(
                row["Payeur"],
                f"{row['Montant (€)']:.2f} €"
            )

        st.subheader("Dépenses par carte")

        df_cartes = df.groupby("Carte")["Montant (€)"].sum().reset_index()
        cols_cartes = st.columns(len(df_cartes))

        for index, row in df_cartes.iterrows():
            cols_cartes[index].metric(
                row["Carte"],
                f"{row['Montant (€)']:.2f} €"
            )

        st.subheader("Budget par catégorie")

        for categorie_budget, budget_max in budgets.items():
            depense_categorie = df[df["Catégorie"] == categorie_budget]["Montant (€)"].sum()
            pourcentage = depense_categorie / budget_max

            st.write(f"{categorie_budget} : {depense_categorie:.2f} € / {budget_max:.2f} €")
            st.progress(min(pourcentage, 1.0))

        st.subheader("📅 Total annuel par catégorie")

        df_year = pd.DataFrame(
            expenses,
            columns=[
                "ID",
                "Date",
                "Catégorie",
                "Montant (€)",
                "Description",
                "Payeur",
                "Carte"
            ]
        )

        years = sorted(
            list(set(df_year["Date"].str[:4])),
            reverse=True
        )

        selected_year = st.selectbox(
            "Année",
            years
        )

        df_year_filtered = df_year[df_year["Date"].str.startswith(selected_year)]

        total_annuel = df_year_filtered["Montant (€)"].sum()

        st.metric("💰 Total annuel", f"{total_annuel:.2f} €")

        df_year_categories = (
            df_year_filtered
            .groupby("Catégorie")["Montant (€)"]
            .sum()
            .reset_index()
            .sort_values("Montant (€)", ascending=False)
        )

        st.dataframe(
            df_year_categories,
            use_container_width=True
        )
with tab_savings:
    st.header("🎯 Objectifs d'épargne")    
    

    with st.form("form_objectif_epargne"):
        nom_objectif = st.text_input("Nom de l'objectif")
        montant_actuel = st.number_input("Montant actuel (€)", min_value=0.0, step=10.0)
        montant_cible = st.number_input("Objectif total (€)", min_value=0.0, step=100.0)

        submitted_goal = st.form_submit_button("Ajouter l'objectif")

        if submitted_goal:
            add_savings_goal(nom_objectif, montant_actuel, montant_cible)
            st.success("✅ Objectif ajouté !")
            st.balloons()

    goals = get_savings_goals()

    if goals:
        for goal in goals:
            goal_id, name, current_amount, target_amount = goal
            pourcentage = current_amount / target_amount if target_amount > 0 else 0

            st.markdown(
                f"**{name}** : {current_amount:.0f} € / {target_amount:.0f} € "
                f"({pourcentage * 100:.1f}%)"
            )

            st.progress(min(pourcentage, 1.0))

            col_amount, col_add, col_100, col_500, col_1000, col_delete = st.columns(
                [2, 1, 1, 1, 1, 1]
            )

            with col_amount:
                amount_to_add = st.number_input(
                "Montant",
                min_value=0.0,
                step=10.0,
                key=f"amount_{goal_id}",
                label_visibility="collapsed"
            )

            with col_add:
                if st.button("➕", key=f"custom_add_{goal_id}"):
                    update_savings_goal_amount(goal_id, current_amount + amount_to_add)
                    st.rerun()

            with col_100:
                if st.button("+100", key=f"add_100_{goal_id}"):
                    update_savings_goal_amount(goal_id, current_amount + 100)
                    st.rerun()

            with col_500:
                if st.button("+500", key=f"add_500_{goal_id}"):
                    update_savings_goal_amount(goal_id, current_amount + 500)
                    st.rerun()

            with col_1000:
                if st.button("+1000", key=f"add_1000_{goal_id}"):
                    update_savings_goal_amount(goal_id, current_amount + 1000)
                    st.rerun()

            with col_delete:
                if st.button("🗑", key=f"delete_goal_{goal_id}"):
                    delete_savings_goal(goal_id)
                    st.rerun()

            st.divider()

with tab_recurring:
    st.header("🔁 Dépenses récurrentes")

    with st.form("form_depense_recurrente"):
        recurring_name = st.text_input("Nom")
        recurring_amount = st.number_input("Montant (€)", min_value=0.0, step=0.01)

        recurring_category = st.selectbox(
            "Catégorie",
            [categories_list],
            key="recurring_category"
        )

        recurring_payer = st.selectbox(
            "Payeur",
            ["Valentin", "Madame", "Commun"],
            key="recurring_payer"
        )

        recurring_card = st.selectbox(
            "Mode de paiement",
            ["Crédit Mutuel", "Trade Republic", "Cash"],
            key="recurring_card"
        )

        recurring_description = st.text_input("Description")

        submitted_recurring = st.form_submit_button("Ajouter la dépense récurrente")

        if submitted_recurring:
            add_recurring_expense(
                recurring_name,
                recurring_amount,
                recurring_category,
                recurring_description,
                recurring_payer,
                recurring_card
            )
            st.success("✅ Dépense récurrente ajoutée")
            st.balloons()

    recurring_expenses = get_recurring_expenses()

    if recurring_expenses:
        recurring_df = pd.DataFrame(
            recurring_expenses,
            columns=[
                "ID",
                "Nom",
                "Montant (€)",
                "Catégorie",
                "Description",
                "Payeur",
                "Carte"
            ]
        )

        st.dataframe(recurring_df, use_container_width=True)
        st.subheader("Générer le mois")

        generation_date = st.date_input(
            "Date des dépenses à générer",
            key="generation_date"
        )

        if st.button("📅 Générer les dépenses récurrentes"):
            for recurring in recurring_expenses:
                recurring_id, name, amount, category, description, payer, card = recurring

                add_expense(
                    str(generation_date),
                    amount,
                    category,
                    description,
                    payer,
                    card
                )

                st.success("✅ Dépenses récurrentes ajoutées au mois")
                st.balloons()
    else:
        st.info("Aucune dépense récurrente pour le moment.")

with tab_settings:
    st.header("⚙️ Paramètres")

    categories_from_db = get_categories()

    if categories_from_db:
        categories_dict = {
            name: budget
            for name, budget in categories_from_db
        }

        selected_category = st.selectbox(
            "Catégorie à modifier",
            list(categories_dict.keys())
        )

        new_budget = st.number_input(
            "Budget mensuel (€)",
            min_value=0.0,
            step=10.0,
            value=float(categories_dict[selected_category])
        )

        if st.button("💾 Modifier le budget"):
            add_or_update_category(selected_category, new_budget)
            st.success("✅ Budget modifié")
            st.rerun()

        if st.button("🗑 Supprimer la catégorie"):
            delete_category(selected_category)
            st.success("✅ Catégorie supprimée")
            st.rerun()
    
    st.subheader("Ajouter une nouvelle catégorie")

    with st.form("form_nouvelle_categorie"):
        category_name = st.text_input("Nom de la catégorie")
        category_budget = st.number_input("Budget mensuel (€)", min_value=0.0, step=10.0)

        submitted_category = st.form_submit_button("Ajouter")

        if submitted_category:
            add_or_update_category(category_name, category_budget)
            st.success("✅ Catégorie ajoutée")
            st.balloons()

    categories_from_db = get_categories()

    if categories_from_db:
        categories_df = pd.DataFrame(
            categories_from_db,
            columns=["Catégorie", "Budget (€)"]
        )

        st.dataframe(categories_df, use_container_width=True)
    else:
        st.info("Aucune catégorie personnalisée pour le moment.")


with tab_history:
    st.header("Historique")

    if df.empty:
        st.info("Aucune dépense enregistrée pour ce mois.")
    else:
        st.dataframe(df, use_container_width=True)

        st.subheader("✏️ Modifier une dépense")

        expense_options = {
            f"{row['ID']} - {row['Date']} - {row['Catégorie']} - {row['Montant (€)']:.2f} €": row["ID"]
            for _, row in df.iterrows()
        }

        selected_expense_label = st.selectbox(
            "Dépense à modifier",
            list(expense_options.keys())
        )

        selected_expense_id = expense_options[selected_expense_label]
        selected_row = df[df["ID"] == selected_expense_id].iloc[0]

        with st.form("form_modifier_depense"):
            edit_date = st.date_input(
                "Date",
                value=pd.to_datetime(selected_row["Date"])
            )

            edit_amount = st.number_input(
                "Montant (€)",
                min_value=0.0,
                step=0.01,
                value=float(selected_row["Montant (€)"])
            )

            edit_category = st.selectbox(
                "Catégorie",
                categories_list,
                index=categories_list.index(selected_row["Catégorie"])
                if selected_row["Catégorie"] in categories_list
                else 0
            )
            

            edit_payer = st.selectbox(
                "Payeur",
                ["Valentin", "Julia", "Commun"],
                index=["Valentin", "Julia", "Commun"].index(selected_row["Payeur"])
            )

            edit_card = st.selectbox(
                "Carte",
                ["Crédit Mutuel", "Trade Republic", "Cash"],
                index=["Crédit Mutuel", "Trade Republic", "Cash"].index(selected_row["Carte"])
            )

            edit_description = st.text_input(
                "Description",
                value=selected_row["Description"]
            )

            submitted_edit = st.form_submit_button("💾 Sauvegarder les modifications")

            if submitted_edit:
                update_expense(
                    selected_expense_id,
                    str(edit_date),
                    edit_amount,
                    edit_category,
                    edit_description,
                    edit_payer,
                    edit_card
                )

                st.success("✅ Dépense modifiée")
                st.rerun()

        st.subheader("Supprimer une dépense")

        expense_id_to_delete = st.number_input(
            "ID de la dépense à supprimer",
            min_value=1,
            step=1
        )

        if st.button("Supprimer"):
            delete_expense(expense_id_to_delete)
            st.success("Dépense supprimée !")
            st.rerun()