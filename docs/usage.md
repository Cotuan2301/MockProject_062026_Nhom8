# Usage Guide: SC-022 Initial Assessment

## 1. Prerequisites
- You must be logged in as a user with the **Nurse** or **Clinical Admin** role.
- The Resident must already be created in the system and assigned to a room.

## 2. Navigating to the Assessment
1. Open the NHMS portal.
2. Click on **Residents** in the left sidebar.
3. Search for and select the resident (e.g., Elena Ramos).
4. Click on **New Admission Flow** and select **Step 3: Initial Assessment**.

## 3. Completing the Form
- **ADL Scoring**: For each of the 8 activities (Bed Mobility, Transfer, etc.), select the appropriate radio button representing the resident's independence level (0 to 4). The subtotal will calculate automatically in real-time.
- **IADL Scoring**: For each instrumental activity, select whether the resident is Dependent (0) or Independent (1).
- **Diagnoses**: 
  - Click **+ Add Diagnosis**.
  - Type the diagnosis name and ICD-10 code.
  - Click **Add**. It will appear as a bullet point in the list.
- **Allergies**: Type allergies separated by commas. If none, leave as "NKDA".
- **Vitals**: Input Blood Pressure (Sys/Dia), Heart Rate, Temperature, Weight, and Height in the provided inline fields.
- **Cognitive Status**: Select the single radio button that best describes the resident's mental status upon admission.
- **Clinical Notes**: Add any narrative observations that support the ADL scoring.

## 4. Saving and Locking
- Click the blue **Save Assessment → triggers LOC calc** button at the bottom of the screen.
- **WARNING**: Once saved, the assessment will be cryptographically signed and locked. You will not be able to edit it. If an error was made, you must contact a Clinical Admin to initiate a formal Amendment.
- Upon successful save, you will be redirected to the Resident Dashboard, and the new Care Level (LOC) will be displayed.
