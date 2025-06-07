from datetime import date
import streamlit as st
import re


required_keys = [
    "resume_ready",
    "generated_resume_path",
    "generated_resume_name",
    "name", "phone", "email", "summary", "college", "cgpa", "education",
    "branch", "startyear", "endyear", "categorized_skills", "experiences",
    "projects", "certifications", "volunteer_experience", "interests",
    "languages_known", "shownext3"
]

for key in required_keys:
    if key not in st.session_state:
        st.session_state[key] = (
            [] if key in ["experiences", "projects", "certifications", "interests", "languages_known"]
            else {} if key == "categorized_skills"
            else False if key in ["resume_ready", "shownext3"]
            else ""
        )

#############################     CSS
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://plus.unsplash.com/premium_photo-1686064771021-fbd6e301a0e4?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTh8fGRhcmslMjBiYWNrZ3JvdW5kfGVufDB8fDB8fHww");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
        height: 100vh; /* Ensure the background covers the whole screen */
    }
    
    </style>
    """,
    unsafe_allow_html=True
)
################################## Title
st.title("Resume Made Easy")
st.subheader("Create ATS Friendly resume with ease")
st.text("Fill in all your Details and Get your Resume Today")
##################################  fUNCTIONS
def is_valid_phone(phone):
    return re.fullmatch(r"[6-9]\d{9}", phone)

def is_valid_email(email):
    return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email)

if "form_page" not in st.session_state:
    st.session_state.form_page = "basic"
    st.session_state.show_next = False
    st.session_state.shownext3 = False
    st.session_state.exp_count = 1
    st.session_state.pro_count = 1
    st.session_state.resume_ready = False

############################ Basic Details 
if st.session_state.form_page == "basic":

    with st.form("Basic Details"):
        name = st.text_input(label="", placeholder="Enter your Full Name")
        job = st.text_input(label="", placeholder="Enter the role you wish for")
        phone = st.text_input(label="", placeholder="Enter your Mobile Number")
        if phone and not is_valid_phone(phone):
            st.warning("❌ Please enter a valid Indian phone number")
        email = st.text_input(label="", placeholder="Enter your Email Address")
        if email and not is_valid_email(email):
            st.warning("❌ Please enter a valid email address")
        summary = st.text_area(label="", placeholder="Describe about yourself")
        submitted = st.form_submit_button("Next")
        if submitted:
            errors = []

            if not name.strip():
                errors.append("Name is required.")
            if not job.strip():
                errors.append("Job role is required.")
            if not is_valid_phone(phone):
                errors.append("❌ Invalid phone number (must be 10 digits starting with 6–9).")
            if not is_valid_email(email):
                errors.append("❌ Invalid email address.")
            if not summary.strip():
                errors.append("Summary is required.")

            if errors:
                for err in errors:
                    st.warning(err)
            else:
                # Save basic details in session_state
                st.session_state.name = name
                st.session_state.job = job
                st.session_state.phone = phone
                st.session_state.email = email
                st.session_state.summary = summary
                st.session_state.form_page = "additional"
                st.session_state.show_next = True

######################    Additional Details 
if st.session_state.form_page == "additional" and st.session_state.show_next:

    st.subheader("Step 2: Additional Details")
    st.markdown("---")

    # Education
    st.markdown("##### Education")
    education_options = [
        "BE / B.Tech",
        "BSc - Computer Science",
        "BSc - Agriculture",
        "B.Com",
        "BBA",
        "BCA",
        "BA",
        "ME / M.Tech",
        "MSc",
        "MBA",
        "Diploma",
        "PhD",
        "Other"
    ]
    education = st.selectbox("Select Your Education", education_options)
    if education == "Other":
        education = st.text_input("Please specify your education")
    if education in education_options:
        college = st.text_input("College Name")
        col1, col2 = st.columns(2)
        branch = col1.text_input("Branch")
        cgpa = col2.text_input("CGPA")
        startyear = col1.number_input("Start Year", min_value=2018, max_value=2026)
        endyear = col2.number_input("End Year", min_value=2020, max_value=2030)

    st.markdown("---")
    st.markdown("##### Work Experience")
    experience_data = []
    for i in range(st.session_state.exp_count):
        st.markdown(f"###### Experience {i+1}")
        col1, col2 = st.columns(2)
        company = col1.text_input("Company Name", key=f"company_{i}")
        role = col2.text_input("Role/Designation", key=f"role_{i}")
        description = st.text_area("Describe your work", key=f"desc_{i}")
        col3, col4 = st.columns(2)
        start_date = col3.date_input("Start Date", key=f"start_{i}", value=date(2021, 1, 1))
        end_date = col4.date_input("End Date", key=f"end_{i}", value=date(2022, 1, 1))
        experience_data.append({
            "company": company,
            "role": role,
            "description": description,
            "start_date": start_date,
            "end_date": end_date
        })

    if st.session_state.exp_count < 3:
        if st.button("➕ Add More Experience"):
            st.session_state.exp_count += 1
    st.session_state.experiences = experience_data

    st.markdown("---")
    st.markdown("##### Skills")

    col1, col2 = st.columns(2)

    with col1:
        prog_langs = st.text_area(
            "Programming Languages",
            placeholder="e.g., Python, Java, C++, JavaScript",
            key="prog_langs"
        )

    with col2:
        frameworks = st.text_area(
            "Frameworks / Libraries",
            placeholder="e.g., React, Django, TensorFlow, NumPy",
            key="frameworks"
        )

    with col1:
        tools = st.text_area(
            "Tools & Platforms",
            placeholder="e.g., Git, Docker, AWS, VS Code",
            key="tools"
        )

    with col2:
        soft_skills = st.text_area(
            "Soft Skills",
            placeholder="e.g., Communication, Teamwork, Problem-Solving",
            key="soft_skills"
        )

    st.session_state.categorized_skills = {
        "Programming Languages": [s.strip() for s in prog_langs.split(",") if s.strip()],
        "Frameworks / Libraries": [s.strip() for s in frameworks.split(",") if s.strip()],
        "Tools & Platforms": [s.strip() for s in tools.split(",") if s.strip()],
        "Soft Skills": [s.strip() for s in soft_skills.split(",") if s.strip()],
    }

    st.markdown("---")
    st.markdown("##### Projects")
    project_data = []
    for i in range(st.session_state.pro_count):
        st.markdown(f"###### Project {i+1}")
        col1, col2 = st.columns(2)
        name = col1.text_input("Enter Title Of Project", key=f"prname_{i}")
        link = col2.text_input("Paste your website Link / Repository Link", key=f"prlink_{i}")
        description = st.text_area("Description", height=68, key=f"prdesc_{i}")
        project_data.append({
            "title": name,
            "link": link,
            "description": description
        })
    st.session_state.projects = project_data
    if st.button("➕ Add More Projects"):
        st.session_state.pro_count += 1

    st.markdown("---")
    form2submit = st.button("Next")
    if form2submit:
        st.session_state.education = education
        st.session_state.college = college
        st.session_state.branch = branch
        st.session_state.cgpa = cgpa
        st.session_state.startyear = startyear
        st.session_state.endyear = endyear
        st.session_state.shownext3 = True
        st.session_state.section3_started = True

############################### Certifications, Interests, etc ---------
if st.session_state.get("section3_started", False):

    st.subheader("Certifications, Interests & Hobbies")

    st.markdown("#### 🏅 Certifications & Achievements")
    certifications = []
    for i in range(5):
        cert = st.text_input(f"Certification / Achievement {i+1}", key=f"cert_{i}")
        if cert.strip():
            certifications.append(cert.strip())

    st.markdown("#### 🙌 Volunteer Experience (Optional)")
    volunteer_exp = st.text_area(
        "Describe any volunteer work or community involvement",
        placeholder="e.g., Taught underprivileged kids, Organized blood donation camp, Led college fest, etc.",
        key="volunteer_exp"
    )

    st.markdown("#### 🎯 Interests & Hobbies")
    interests_input = st.text_input(
        "Enter your interests (comma-separated)",
        placeholder="e.g., AI, Space, Innovation",
        key="interests_input"  # Key changed to avoid clash
    )

    st.markdown("#### 🌐 Languages Known")
    languages_input = st.text_input(
        "Enter the languages you know (comma-separated)",
        placeholder="e.g., English, Hindi, Telugu, Tamil",
        key="languages_input"  # Key changed
    )

    if st.button("✅ Submit"):

        st.session_state.certifications = certifications
        st.session_state.volunteer_experience = volunteer_exp.strip()
        st.session_state.interests = [i.strip() for i in interests_input.split(",") if i.strip()]
        st.session_state.languages_known = [lang.strip() for lang in languages_input.split(",") if lang.strip()]
        st.session_state.resume_ready = True  # Mark ready

        st.success("🎉 Resume Data Captured Successfully!")

# --------- Generate Resume if ready ---------
if st.session_state.get("resume_ready", False):
    from resumeapp import generate_resume
    generate_resume()
