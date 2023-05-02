

class Resume:
    def __init__(self, name, email, location, phone, summary, experience, education, skills, certifications, personal_projects):
        self.name = name
        self.email = email
        self.phone = phone
        self.location = location
        self.summary = summary
        self.experience = experience
        self.education = education
        self.skills = skills
        self.certifications = certifications
        self.personal_projects = personal_projects

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'summary': self.summary,
            'experience': self.experience,
            'Education': self.education,
            'skills': self.skills,
            'certifications': self.certifications,
            'personal_projects': self.personal_projects

        }


class JobDescription:
    def __init__(self, title, company, location, description, requirements, qualifications):
        self.title = title
        self.company = company
        self.location = location
        self.description = description
        self.requirements = requirements
        self.qualifications = qualifications

    def to_dict(self):
        return {
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'description': self.description,
            'requirements': self.requirements,
            'qualifications': self.qualifications
        }
