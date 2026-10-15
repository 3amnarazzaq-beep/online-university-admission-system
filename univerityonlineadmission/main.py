class UniversityAdmissionSystem:
    def __init__(self):
        self.files = [
            "personal.txt", "guardian.txt", "address.txt",
            "education.txt", "program.txt", "documents.txt", "status.txt"
        ]
        self.create_files()

    def create_files(self):
        for file_name in self.files + ["sequence.txt"]:
            try:
                with open(file_name, "a", encoding="utf-8"):
                    pass
            except OSError as error:
                print("Could not create", file_name, ":", error)

    def clean(self, value):
        return str(value).strip().replace("|", "/").replace("\n", " ")

    def read_records(self, file_name):
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                return [line.rstrip("\n").split("|") for line in file if line.strip()]
        except FileNotFoundError:
            return []

    def write_records(self, file_name, records):
        with open(file_name, "w", encoding="utf-8") as file:
            for record in records:
                file.write("|".join(self.clean(value) for value in record) + "\n")

    def append_record(self, file_name, record):
        with open(file_name, "a", encoding="utf-8") as file:
            file.write("|".join(self.clean(value) for value in record) + "\n")

    def get_application_id(self):
        try:
            with open("sequence.txt", "r", encoding="utf-8") as file:
                last_number = int(file.read().strip() or "0")
        except (FileNotFoundError, ValueError):
            last_number = 0

        # Also check saved records in case sequence.txt was removed or reset.
        for record in self.read_records("personal.txt"):
            if record and record[0].startswith("ADM-2026-"):
                try:
                    last_number = max(last_number, int(record[0].split("-")[-1]))
                except ValueError:
                    pass

        new_number = last_number + 1
        with open("sequence.txt", "w", encoding="utf-8") as file:
            file.write(str(new_number))
        return "ADM-2026-" + str(new_number).zfill(4)

    def get_text(self, message):
        while True:
            value = self.clean(input(message))
            if value:
                return value
            print("This field cannot be empty.")

    def get_yes_no(self, message):
        while True:
            answer = input(message).strip().lower()
            if answer in ("yes", "y"):
                return "Yes"
            if answer in ("no", "n"):
                return "No"
            print("Please enter Yes or No.")

    def get_choice(self, message, choices):
        while True:
            answer = input(message).strip()
            if answer in choices:
                return answer
            print("Please choose one of:", ", ".join(choices))

    def get_number(self, message, minimum=0):
        while True:
            try:
                number = float(input(message))
                if number >= minimum:
                    return number
                print("Enter a number equal to or greater than", minimum)
            except ValueError:
                print("Please enter a valid number.")

    def get_date(self, message):
        from datetime import datetime
        while True:
            value = self.get_text(message)
            try:
                datetime.strptime(value, "%d-%m-%Y")
                return value
            except ValueError:
                print("Use DD-MM-YYYY format, for example 24-07-2006.")

    def get_phone(self, message):
        while True:
            value = self.get_text(message)
            digits = "".join(character for character in value if character.isdigit())
            if len(digits) >= 10:
                return value
            print("Enter a valid phone number with at least 10 digits.")

    def get_cnic(self, message):
        while True:
            value = self.get_text(message)
            digits = "".join(character for character in value if character.isdigit())
            if len(digits) == 13:
                return value
            print("Enter a CNIC/B-Form number containing 13 digits.")

    def get_address(self, title):
        print("\n---", title, "---")
        return [
            self.get_text("House/Street: "),
            self.get_text("Area/Village: "),
            self.get_text("City: "),
            self.get_text("District: "),
            self.get_text("Tehsil: "),
            self.get_text("Province: "),
            self.get_text("Postal Code: ")
        ]

    def get_education_record(self, application_id, qualification):
        print("\n---", qualification, "Information ---")
        board = self.get_text("Board/University: ")
        institution = self.get_text("Institution: ")
        year = self.get_text("Passing Year: ")
        total_marks = self.get_number("Total Marks: ", 1)
        obtained_marks = self.get_number("Obtained Marks: ", 0)
        while obtained_marks > total_marks:
            print("Obtained marks cannot be greater than total marks.")
            obtained_marks = self.get_number("Obtained Marks: ", 0)
        percentage = round((obtained_marks / total_marks) * 100, 2)
        grade = self.get_text("Grade: ")
        roll_number = self.get_text("Roll Number: ")
        print("Calculated Percentage:", percentage, "%")
        return [
            application_id, qualification, board, institution, year,
            total_marks, obtained_marks, percentage, grade, roll_number
        ]

    def collect_application(self, application_id):
        print("\n--- Personal Information ---")
        personal = [
            application_id,
            self.get_text("Full Name: "),
            self.get_text("Father's Name: "),
            self.get_text("Mother's Name: "),
            self.get_date("Date of Birth (DD-MM-YYYY): "),
            self.get_choice("Gender (Male/Female/Other): ", ["Male", "Female", "Other"]),
            self.get_cnic("CNIC/B-Form (13 digits): "),
            self.get_text("Nationality: "),
            self.get_text("Religion: "),
            self.get_phone("Mobile Number: "),
            self.get_phone("WhatsApp Number: "),
            self.get_text("Email: "),
            self.get_text("Domicile Province: "),
            self.get_text("Domicile District: "),
            self.get_choice("Blood Group (A+, A-, B+, B-, AB+, AB-, O+, O-): ",
                            ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]),
            self.get_choice("Disability Status (Yes/No): ", ["Yes", "No"]),
            self.get_text("Additional Information (enter None if not applicable): ")
        ]
        while "@" not in personal[11] or "." not in personal[11].split("@")[-1]:
            print("Please enter a valid email address.")
            personal[11] = self.get_text("Email: ")

        print("\n--- Father/Guardian Information ---")
        guardian = [
            application_id,
            self.get_text("Father/Guardian Name: "),
            self.get_cnic("Father/Guardian CNIC (13 digits): "),
            self.get_phone("Guardian Mobile Number: "),
            self.get_text("Guardian Occupation: "),
            self.get_number("Monthly Income: ", 0),
            self.get_text("Relationship with Applicant: "),
            self.get_text("Guardian Address: ")
        ]

        permanent_address = self.get_address("Permanent Address")
        if self.get_yes_no("Is your current address the same as your permanent address? (Yes/No): ") == "Yes":
            current_address = permanent_address.copy()
        else:
            current_address = self.get_address("Current Address")

        address_records = [
            [application_id, "Permanent"] + permanent_address,
            [application_id, "Current"] + current_address
        ]

        education_records = [
            self.get_education_record(application_id, "Matric/SSC"),
            self.get_education_record(application_id, "Intermediate/HSSC")
        ]
        while self.get_yes_no("Do you want to add another qualification? (Yes/No): ") == "Yes":
            qualification = self.get_text("Qualification name: ")
            education_records.append(self.get_education_record(application_id, qualification))

        programs = [
            "BS Computer Science", "BS Software Engineering",
            "BS Information Technology", "BS Artificial Intelligence",
            "BBA", "BS Accounting & Finance", "BS English", "BS Mathematics"
        ]
        print("\n--- Program Preferences ---")
        for index, program in enumerate(programs, 1):
            print(str(index) + ".", program)
        preferences = []
        for label in ("First", "Second", "Third"):
            while True:
                choice = self.get_choice(label + " Preference (1-8): ", [str(i) for i in range(1, 9)])
                if choice not in preferences:
                    preferences.append(choice)
                    break
                print("Please select a different program for each preference.")
        program_record = [
            application_id,
            programs[int(preferences[0]) - 1],
            programs[int(preferences[1]) - 1],
            programs[int(preferences[2]) - 1],
            self.get_text("Campus: "),
            self.get_choice("Shift (Morning/Evening): ", ["Morning", "Evening"]),
            self.get_text("Admission Category: ")
        ]

        document_names = [
            "CNIC/B-Form", "Father/Guardian CNIC", "Matric Certificate",
            "Matric DMC", "Intermediate Certificate", "Intermediate DMC",
            "Domicile", "Passport Photograph", "Character Certificate",
            "Entry Test Result", "Equivalence Certificate (if applicable)",
            "Migration Certificate (if applicable)"
        ]
        print("\n--- Document Checklist ---")
        document_records = []
        for document in document_names:
            provided = self.get_yes_no(document + " provided? (Yes/No): ")
            document_records.append([application_id, document, provided])

        return {
            "personal": personal,
            "guardian": guardian,
            "address": address_records,
            "education": education_records,
            "program": program_record,
            "documents": document_records,
            "status": [application_id, "Submitted"]
        }

    def show_application_data(self, data):
        print("\n========== APPLICATION REVIEW ==========")
        labels = [
            "Application ID", "Full Name", "Father's Name", "Mother's Name",
            "Date of Birth", "Gender", "CNIC/B-Form", "Nationality", "Religion",
            "Mobile Number", "WhatsApp Number", "Email", "Domicile Province",
            "Domicile District", "Blood Group", "Disability Status", "Additional Information"
        ]
        for label, value in zip(labels, data["personal"]):
            print(label + ":", value)

        print("\nGuardian Information:")
        for label, value in zip(
            ["Guardian Name", "Guardian CNIC", "Guardian Mobile", "Occupation",
             "Monthly Income", "Relationship", "Guardian Address"],
            data["guardian"][1:]
        ):
            print(label + ":", value)

        print("\nAddresses:")
        for record in data["address"]:
            print(record[1] + " Address:", ", ".join(record[2:]))

        print("\nEducation:")
        for record in data["education"]:
            print(
                record[1] + " | Board/University:", record[2],
                "| Institution:", record[3], "| Year:", record[4],
                "| Total Marks:", record[5], "| Obtained Marks:", record[6],
                "| Percentage:", record[7], "% | Grade:", record[8],
                "| Roll Number:", record[9]
            )

        record = data["program"]
        print("\nProgram Preferences:")
        print("First:", record[1], "| Second:", record[2], "| Third:", record[3])
        print("Campus:", record[4], "| Shift:", record[5], "| Category:", record[6])

        print("\nDocuments:")
        for record in data["documents"]:
            print(record[1] + ":", record[2])
        print("\nDeclaration:")
        print('"I declare that the information provided by me is true and correct to the best of my knowledge."')

    def save_application(self, data):
        # Save all sections only after the applicant agrees to the declaration.
        for file_name, key in [
            ("personal.txt", "personal"),
            ("guardian.txt", "guardian"),
            ("address.txt", "address"),
            ("education.txt", "education"),
            ("program.txt", "program"),
            ("documents.txt", "documents"),
            ("status.txt", "status")
        ]:
            records = data[key]
            if key not in ("address", "education", "documents"):
                records = [records]
            for record in records:
                self.append_record(file_name, record)

    def new_application(self):
        application_id = self.get_application_id()
        print("\nNew Application ID:", application_id)
        try:
            while True:
                data = self.collect_application(application_id)
                self.show_application_data(data)
                action = self.get_choice(
                    "\nChoose: 1 Submit, 2 Edit (re-enter details), 3 Cancel: ",
                    ["1", "2", "3"]
                )
                if action == "2":
                    print("Please re-enter the application details.")
                    continue
                if action == "3":
                    print("Application cancelled. No application details were saved.")
                    return
                declaration = self.get_yes_no("Do you agree with the declaration? (Yes/No): ")
                if declaration == "No":
                    print("Application was not submitted.")
                    return
                self.save_application(data)
                print("\nApplication submitted successfully.")
                print("Application ID:", application_id)
                return
        except (OSError, KeyboardInterrupt) as error:
            print("\nApplication could not be completed:", error)

    def get_application(self, application_id):
        data = {}
        for key, file_name in [
            ("personal", "personal.txt"), ("guardian", "guardian.txt"),
            ("address", "address.txt"), ("education", "education.txt"),
            ("program", "program.txt"), ("documents", "documents.txt"),
            ("status", "status.txt")
        ]:
            data[key] = [record for record in self.read_records(file_name)
                         if record and record[0] == application_id]
        return data if data["personal"] else None

    def search_application(self):
        application_id = self.get_text("Enter Application ID: ")
        data = self.get_application(application_id)
        if data:
            record = data["personal"][0]
            print("Application Found")
            print("Application ID:", record[0])
            print("Name:", record[1])
            print("CNIC/B-Form:", record[6])
            print("Mobile:", record[9])
        else:
            print("Application not found.")

    def view_application(self):
        application_id = self.get_text("Enter Application ID: ")
        data = self.get_application(application_id)
        if not data:
            print("Application not found.")
            return
        print("\n========== SAVED APPLICATION ==========")
        personal_labels = [
            "Application ID", "Full Name", "Father's Name", "Mother's Name",
            "Date of Birth", "Gender", "CNIC/B-Form", "Nationality", "Religion",
            "Mobile Number", "WhatsApp Number", "Email", "Domicile Province",
            "Domicile District", "Blood Group", "Disability Status", "Additional Information"
        ]
        for label, value in zip(personal_labels, data["personal"][0]):
            print(label + ":", value)
        for title, key in [
            ("Guardian", "guardian"), ("Addresses", "address"),
            ("Education", "education"), ("Program", "program"),
            ("Documents", "documents"), ("Status", "status")
        ]:
            print("\n" + title + ":")
            for record in data[key]:
                print(" | ".join(record[1:]))

    def replace_application_records(self, application_id, file_name, new_records):
        records = self.read_records(file_name)
        records = [record for record in records if not record or record[0] != application_id]
        records.extend(new_records)
        self.write_records(file_name, records)

    def update_application(self):
        application_id = self.get_text("Enter Application ID: ")
        data = self.get_application(application_id)
        if not data:
            print("Application not found.")
            return

        print("Update which section?")
        print("1. Personal information")
        print("2. Guardian information")
        print("3. Permanent/current address")
        print("4. Education (re-enter all qualifications)")
        print("5. Program preferences")
        print("6. Document checklist")
        print("7. Application status")
        section = self.get_choice("Choose 1-7: ", [str(i) for i in range(1, 8)])

        if section == "1":
            record = data["personal"][0]
            fields = [
                "Full Name", "Father's Name", "Mother's Name", "Date of Birth (DD-MM-YYYY)",
                "Gender", "CNIC/B-Form", "Nationality", "Religion", "Mobile Number",
                "WhatsApp Number", "Email", "Domicile Province", "Domicile District",
                "Blood Group", "Disability Status", "Additional Information"
            ]
            for index, field in enumerate(fields, 1):
                print(str(index) + ".", field, "=", record[index])
            index = int(self.get_choice("Field number to update (1-16): ",
                                        [str(i) for i in range(1, 17)]))
            record[index] = self.get_text("New " + fields[index - 1] + ": ")
            self.replace_application_records(application_id, "personal.txt", [record])

        elif section == "2":
            record = data["guardian"][0]
            fields = ["Guardian Name", "Guardian CNIC", "Guardian Mobile", "Occupation",
                      "Monthly Income", "Relationship", "Guardian Address"]
            for index, field in enumerate(fields, 1):
                print(str(index) + ".", field, "=", record[index])
            index = int(self.get_choice("Field number to update (1-7): ",
                                        [str(i) for i in range(1, 8)]))
            record[index] = self.get_text("New " + fields[index - 1] + ": ")
            self.replace_application_records(application_id, "guardian.txt", [record])

        elif section == "3":
            address_type = self.get_choice("Which address? (Permanent/Current): ",
                                           ["Permanent", "Current"])
            record = next((r for r in data["address"] if len(r) > 1 and r[1] == address_type), None)
            if not record:
                print("Address record not found.")
                return
            fields = ["House/Street", "Area/Village", "City", "District", "Tehsil", "Province", "Postal Code"]
            for index, field in enumerate(fields, 2):
                print(str(index - 1) + ".", field, "=", record[index])
            index = int(self.get_choice("Field number to update (1-7): ",
                                        [str(i) for i in range(1, 8)])) + 1
            record[index] = self.get_text("New " + fields[index - 2] + ": ")
            self.replace_application_records(application_id, "address.txt", data["address"][:])
            records = self.read_records("address.txt")
            # Rebuild this application's address rows with the edited row.
            records = [r for r in records if not r or r[0] != application_id]
            records.extend(data["address"])
            self.write_records("address.txt", records)

        elif section == "4":
            new_records = []
            new_records.append(self.get_education_record(application_id, "Matric/SSC"))
            new_records.append(self.get_education_record(application_id, "Intermediate/HSSC"))
            while self.get_yes_no("Add another qualification? (Yes/No): ") == "Yes":
                qualification = self.get_text("Qualification name: ")
                new_records.append(self.get_education_record(application_id, qualification))
            self.replace_application_records(application_id, "education.txt", new_records)

        elif section == "5":
            programs = [
                "BS Computer Science", "BS Software Engineering",
                "BS Information Technology", "BS Artificial Intelligence",
                "BBA", "BS Accounting & Finance", "BS English", "BS Mathematics"
            ]
            for index, program in enumerate(programs, 1):
                print(str(index) + ".", program)
            choices = []
            for label in ("First", "Second", "Third"):
                while True:
                    choice = self.get_choice(label + " preference (1-8): ",
                                              [str(i) for i in range(1, 9)])
                    if choice not in choices:
                        choices.append(choice)
                        break
                    print("Choose a different program.")
            record = [
                application_id, programs[int(choices[0]) - 1],
                programs[int(choices[1]) - 1], programs[int(choices[2]) - 1],
                self.get_text("Campus: "),
                self.get_choice("Shift (Morning/Evening): ", ["Morning", "Evening"]),
                self.get_text("Admission Category: ")
            ]
            self.replace_application_records(application_id, "program.txt", [record])

        elif section == "6":
            names = [record[1] for record in data["documents"]]
            updated = []
            for name in names:
                answer = self.get_yes_no(name + " provided? (Yes/No): ")
                updated.append([application_id, name, answer])
            self.replace_application_records(application_id, "documents.txt", updated)

        elif section == "7":
            status = self.get_choice(
                "Status (Submitted/Under Review/Eligible/Ineligible/Accepted/Rejected): ",
                ["Submitted", "Under Review", "Eligible", "Ineligible", "Accepted", "Rejected"]
            )
            self.replace_application_records(application_id, "status.txt", [[application_id, status]])

        print("Application updated successfully.")

    def delete_application(self):
        application_id = self.get_text("Enter Application ID: ")
        data = self.get_application(application_id)
        if not data:
            print("Application not found.")
            return
        if self.get_yes_no("Are you sure you want to delete this application? (Yes/No): ") == "No":
            print("Deletion cancelled.")
            return
        for file_name in self.files:
            records = self.read_records(file_name)
            records = [record for record in records if not record or record[0] != application_id]
            self.write_records(file_name, records)
        print("Application deleted successfully.")

    def display_all(self):
        records = self.read_records("personal.txt")
        if not records:
            print("No applications found.")
            return
        print("\n========== ALL APPLICATIONS ==========")
        for record in records:
            if len(record) >= 10:
                print("Application ID:", record[0])
                print("Name:", record[1])
                print("CNIC/B-Form:", record[6])
                print("Mobile:", record[9])
                print("-" * 35)

    def application_status(self):
        application_id = self.get_text("Enter Application ID: ")
        records = [record for record in self.read_records("status.txt")
                   if record and record[0] == application_id]
        if records:
            print("Application Status:", records[-1][1])
        else:
            print("Application not found.")

    def main(self):
        while True:
            print("\n==========================================")
            print("      ONLINE UNIVERSITY ADMISSION SYSTEM")
            print("==========================================")
            print("1. New Application")
            print("2. Search Application")
            print("3. View Application")
            print("4. Update Application")
            print("5. Delete Application")
            print("6. Display All Applications")
            print("7. Application Status")
            print("8. Exit")
            choice = input("Enter your choice: ").strip()

            try:
                if choice == "1":
                    self.new_application()
                elif choice == "2":
                    self.search_application()
                elif choice == "3":
                    self.view_application()
                elif choice == "4":
                    self.update_application()
                elif choice == "5":
                    self.delete_application()
                elif choice == "6":
                    self.display_all()
                elif choice == "7":
                    self.application_status()
                elif choice == "8":
                    print("Program ended.")
                    break
                else:
                    print("Invalid choice. Please enter 1-8.")
            except (OSError, ValueError, IndexError) as error:
                print("An error occurred:", error)


if __name__ == "__main__":
    system = UniversityAdmissionSystem()
    system.main()
