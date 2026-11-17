
import streamlit as st
import logging
from datetime import date

from langchain.agents import create_agent
from langchain.messages import HumanMessage

from agents import delegate_to_subagent1, delegate_to_subagent2
from models import llm_model
from prompt import WEDDING_PLANNER_AGENT_PROMPT, USER_PROMPT_FOR_MAIN_AGENT


# ==========================================================
# CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="AI Wedding Planner",
    page_icon="💍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

/* Main application */
.stApp {
    background: linear-gradient(120deg, #100f1b 0%, #1b1526 55%, #24152a 100%);
    color: #f8f3f7;
}

/* Full width */
.block-container {
    max-width: 100% !important;
    padding: 0.5rem 2rem 1rem !important;
}

/* Hide default elements */
header, footer {
    visibility: hidden;
}

/* Hero */
.hero {
    text-align: center;
    padding: 5px 0 14px;
}

.hero-icon {
    font-size: 35px;
}

.hero h1 {
    font-size: 32px;
    font-weight: 800;
    color: #f5c9dd;
    margin: 0;
}

.hero p {
    font-size: 13px;
    color: #c9b9c9;
    margin-top: 5px;
}

/* Form container */
.stForm {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(246,202,221,0.2);
    border-radius: 16px;
    padding: 15px 20px;
}

/* Section headings */
.section-title {
    font-size: 17px;
    font-weight: 750;
    color: #f6cadd;
    margin: 4px 0 8px;
}

.section-description {
    font-size: 11px;
    color: #b9a9ba;
    margin-bottom: 8px;
}

/* Compact vertical spacing */
div[data-testid="stVerticalBlock"] {
    gap: 0.45rem;
}

/* Labels */
.stTextInput label,
.stSelectbox label,
.stNumberInput label,
.stDateInput label,
.stRadio label,
.stSlider label,
.stCheckbox label,
.stTextArea label {
    font-size: 12px !important;
}

/* Inputs */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    border-radius: 9px !important;
}

/* Buttons */
.stFormSubmitButton button {
    background: linear-gradient(90deg, #d66c9c, #a65cbb);
    color: white;
    border: none;
    border-radius: 11px;
    height: 44px;
    font-weight: 750;
    transition: 0.2s;
}

.stFormSubmitButton button:hover {
    background: linear-gradient(90deg, #e58bb3, #bd78cf);
    color: white;
    transform: translateY(-2px);
}

/* Separators */
hr {
    border-color: rgba(246,202,221,0.15);
    margin: 8px 0 !important;
}

/* Result */
.result-header {
    text-align: center;
    padding: 20px 0;
}

.result-header h2 {
    font-size: 30px;
    color: #f5c9dd;
}

.result-header p {
    color: #c9b9c9;
    font-size: 14px;
}

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    padding: 12px;
    border-radius: 12px;
}

/* Result panel */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 16px;
    border-color: rgba(246,202,221,0.2);
}

/* Mobile */
@media (max-width: 768px) {
    .block-container {
        padding: 0.5rem 0.8rem !important;
    }

    .hero h1 {
        font-size: 24px;
    }

    .stForm {
        padding: 12px;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# HERO SECTION
# ==========================================================

st.markdown("""
<div class="hero">
    <div class="hero-icon">💍</div>
    <h1>AI Wedding Planner</h1>
    <p>
        Your personal AI wedding planning team.
        Design your dream wedding with intelligent multi-agent assistance.
    </p>
</div>
""", unsafe_allow_html=True)


# ==========================================================
# WEDDING FORM
# ==========================================================

with st.form("wedding_planning_form"):

    left, right = st.columns([1, 1], gap="large")

    # ------------------------------------------------------
    # LEFT COLUMN: WEDDING DETAILS
    # ------------------------------------------------------

    with left:

        st.markdown(
            '<div class="section-title">💍 Wedding Essentials</div>',
            unsafe_allow_html=True
        )

        wedding_location = st.text_input(
            "📍 Wedding Location",
            placeholder="Example: Tozeur, Tunisia"
        )

        col1, col2 = st.columns(2)

        with col1:
            guests = st.number_input(
                "👥 Number of Guests",
                min_value=1,
                max_value=5000,
                value=150,
                step=10
            )

        with col2:
            wedding_type = st.selectbox(
                "💒 Wedding Type",
                [
                    "Traditional Wedding",
                    "Luxury Wedding",
                    "Modern Wedding",
                    "Beach Wedding",
                    "Outdoor Wedding",
                    "Destination Wedding",
                    "Intimate Wedding"
                ]
            )

        col1, col2 = st.columns(2)

        with col1:
            wedding_style = st.selectbox(
                "🎨 Wedding Style",
                [
                    "Elegant & Minimalist",
                    "Luxury & Glamorous",
                    "Romantic & Floral",
                    "Rustic & Bohemian",
                    "Traditional & Cultural",
                    "Modern & Contemporary",
                    "Vintage"
                ]
            )

        with col2:
            atmosphere = st.selectbox(
                "✨ Desired Atmosphere",
                [
                    "Romantic",
                    "Elegant",
                    "Festive & Energetic",
                    "Relaxed & Intimate"
                ]
            )

        date_not_decided = st.checkbox(
            "Wedding date not decided yet"
        )

        wedding_date = st.date_input(
            "📅 Wedding Date",
            value=date.today(),
            min_value=date.today(),
            disabled=date_not_decided
        )

        st.markdown(
            '<div class="section-title">💰 Wedding Budget</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([2, 1])

        with col1:
            budget = st.slider(
                "Estimated Total Budget",
                min_value=500,
                max_value=100000,
                value=10000,
                step=500
            )

        with col2:
            currency = st.selectbox(
                "Currency",
                ["TND", "USD", "EUR"]
            )

        st.caption(
            f"Estimated budget: {budget:,} {currency}"
        )

    # ------------------------------------------------------
    # RIGHT COLUMN: SERVICES
    # ------------------------------------------------------

    with right:

        st.markdown(
            '<div class="section-title">🏛️ Venue & Services</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:

            venue_type = st.selectbox(
                "🏛️ Preferred Venue",
                [
                    "Luxury Hotel",
                    "Wedding Hall",
                    "Outdoor Garden",
                    "Beach",
                    "Private Villa",
                    "Desert Location",
                    "Restaurant",
                    "Not Decided"
                ]
            )

            decoration = st.selectbox(
                "🌸 Decoration",
                [
                    "Luxury Floral Decoration",
                    "Minimalist Decoration",
                    "Traditional Decoration",
                    "Modern Decoration",
                    "Bohemian Decoration",
                    "Not Decided"
                ]
            )

            catering = st.selectbox(
                "🍽️ Catering",
                [
                    "Traditional Cuisine",
                    "International Cuisine",
                    "Buffet",
                    "Fine Dining",
                    "Mixed Cuisine",
                    "Not Decided"
                ]
            )

        with col2:

            photography = st.selectbox(
                "📸 Photography & Video",
                [
                    "Photography + Cinematic Video",
                    "Professional Photography",
                    "Photography + Drone",
                    "Full Wedding Coverage",
                    "Not Required"
                ]
            )

            music = st.selectbox(
                "🎵 Entertainment",
                [
                    "Live Band",
                    "DJ",
                    "Traditional Music",
                    "Live Band + DJ",
                    "Not Decided"
                ]
            )

            accommodation = st.selectbox(
                "🏨 Guest Accommodation",
                [
                    "Required",
                    "Not Required",
                    "Optional / Recommendations Only"
                ]
            )

        st.markdown(
            '<div class="section-title">💎 Additional Services</div>',
            unsafe_allow_html=True
        )

        services = [
            "Wedding Coordinator",
            "Makeup & Hairstyling",
            "Wedding Cake",
            "Flowers & Bouquet",
            "Transportation",
            "Invitations",
            "Honeymoon Planning",
            "Drone Coverage",
            "Fireworks"
        ]

        selected_services = []

        service_cols = st.columns(3)

        for i, service in enumerate(services):

            with service_cols[i % 3]:

                if st.checkbox(
                    service,
                    key=f"service_{i}"
                ):
                    selected_services.append(service)

        st.markdown(
            '<div class="section-title">📝 Special Requests</div>',
            unsafe_allow_html=True
        )

        additional_requirements = st.text_area(
            "Additional Requirements",
            placeholder=(
                "Describe your dream wedding, "
                "special preferences, cultural traditions..."
            ),
            height=75
        )

    # ------------------------------------------------------
    # SUBMIT
    # ------------------------------------------------------

    st.markdown("---")

    submitted = st.form_submit_button(
        "✨ GENERATE MY WEDDING PLAN",
        type="primary",
        use_container_width=True
    )


# ==========================================================
# GENERATE WEDDING PLAN
# ==========================================================

if submitted:

    if not wedding_location.strip():

        st.warning("Please enter your wedding location.")

    else:

        # Construct requirements
        requirements = f"""
WEDDING DETAILS
- Location: {wedding_location}
- Wedding Type: {wedding_type}
- Wedding Date: {"Not decided yet" if date_not_decided else wedding_date}
- Number of Guests: {guests}
- Wedding Style: {wedding_style}
- Desired Atmosphere: {atmosphere}

BUDGET
- Total Budget: {budget:,} {currency}

VENUE AND SERVICES
- Venue: {venue_type}
- Decoration: {decoration}
- Catering: {catering}
- Photography and Video: {photography}
- Entertainment: {music}
- Accommodation: {accommodation}

ADDITIONAL SERVICES
{", ".join(selected_services) if selected_services else "None selected"}

SPECIAL REQUESTS
{additional_requirements.strip() if additional_requirements.strip() else "No additional requirements."}

INSTRUCTIONS
Create a detailed and realistic wedding plan.
Respect the user's budget, location and guest count.
Include practical recommendations, estimated costs and a complete timeline.
Clearly identify assumptions and prices that require local verification.
"""

        with st.spinner(
            "💍 Your AI wedding planning agents are working..."
        ):

            try:

                logging.info("Starting wedding planning workflow")

                # Build system prompt
                new_system_prompt = WEDDING_PLANNER_AGENT_PROMPT.format(
                    requirements=requirements
                )

                # Create main agent
                main_agent = create_agent(
                    model=llm_model,
                    tools=[
                        delegate_to_subagent1,
                        delegate_to_subagent2
                    ],
                    name="MainWeddingPlannerAgent",
                    system_prompt=new_system_prompt
                )

                # Invoke agent
                result = main_agent.invoke({
                    "messages": [
                        HumanMessage(
                            content=USER_PROMPT_FOR_MAIN_AGENT
                        )
                    ]
                })

                # Extract response
                final_response = result["messages"][-1].content

                # Handle content blocks
                if isinstance(final_response, list):

                    final_response = "\n".join(
                        block.get("text", str(block))
                        if isinstance(block, dict)
                        else str(block)
                        for block in final_response
                    )

                # Save result
                st.session_state["wedding_plan"] = final_response

                st.success("Your wedding plan has been generated!")

                logging.info("Wedding planning completed")

            except Exception as e:

                logging.exception("Wedding planning failed")

                st.error(f"An error occurred: {str(e)}")


# ==========================================================
# DISPLAY AI RESULTS
# ==========================================================

if st.session_state.get("wedding_plan"):

    st.markdown("---")

    st.markdown("""
    <div class="result-header">
        <div style="font-size:42px;">✨💍</div>
        <h2>Your Wedding Plan Is Ready!</h2>
        <p>Your personalized wedding proposal, prepared by your AI agents.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):

        st.markdown(
            st.session_state["wedding_plan"]
        )

    st.download_button(
        label="📥 Download Your Wedding Plan",
        data=st.session_state["wedding_plan"],
        file_name="wedding_plan.md",
        mime="text/markdown",
        use_container_width=True
    )

    if st.button("🔄 Create Another Wedding Plan"):

        del st.session_state["wedding_plan"]
        st.rerun()
