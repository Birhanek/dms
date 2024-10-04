from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import relationship
from uuid import uuid4, UUID
from datetime import datetime
from flask_login import UserMixin
from . import Base

class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(String(50),primary_key=True, default=lambda: str(uuid4()))
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(200),unique=True,nullable=False)
    password = Column(String(200),nullable=False)
    role = Column(String(100),nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    last_login = Column(DateTime)

    #Relationships
    documents = relationship('Document', back_populates='uploader')
    audits = relationship('Audit', back_populates='user')
    permissions = relationship('Permission', back_populates='user')
    # New
    students = relationship('Student', back_populates='user')
    consultants = relationship('Consultant',back_populates='users')

# Students table -> stores detailed information about students.
class Student(Base):
    __tablename__ = 'students'

    id = Column(String(50), primary_key=True, default=lambda: str(datetime.now().year) + "-" + str(uuid4()))
    first_name = Column(String(255), nullable=False )
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    phone_number = Column(String(100), nullable=False)
    education_level = Column(String(100), nullable=False)
    country_of_residence = Column(String(100),nullable=False)
    country_of_interest = Column(String(100))
    field_of_study_interest = Column(String(255))
    user_id = Column(String(50), ForeignKey('users.id'))

    #Relationships
    user = relationship('User', back_populates='students')
    consult = relationship('Consultation', back_populates='student')
    payment = relationship('Payment', back_populates='students')

# Tracks consultations between students and consultants.
class Consultation(Base):
    id = Column(String(50), primary_key=True, default=lambda: str(uuid4()))
    student_id= Column(String(50),ForeignKey('students.id'))
    consultant_id=Column(String(50), ForeignKey('consultants.id'))
    scheduled_date= Column(DateTime)
    duration = Column(Integer)  # Consultation duration
    notes=Column(Text) # consultation notes

    # Relationship
    students=relationship('Student', back_populates='consult')


# Tracks payments made by students for consultancy services or application fees.
class Payment(Base):
    id = Column(String(36), primary_key=True, default=lambda:str(uuid4()))
    student_id = Column(String(50), ForeignKey('students.id'))
    amount=Column(Integer,nullable=False)
    currency=Column(String(20), nullable=False)
    payment_method= Column(String(30), nullable=False)
    payment_date=Column(DateTime, nullable=False)
    status=Column(String(20), nullable=False)

    # Relation
    students= relationship('Student', back_populates='payment')

class Consultant(Base):
    id=Column(String(36), primary_key=True, default=lambda:str(uuid4()))
    user_id= Column(String(50), ForeignKey('users.id'))
    first_name=Column(String(100),nullable=False)
    last_name=Column(String(100),nullable=False)
    specialization=Column(String(200), nullable=False)
    years_of_experience=Column(Integer,nullable=False, default=0)
    languages_spoken=Column(String(100))
    rating = Column(Integer)

    # Relationship
    users = relationship('User',back_populates='consultants')

class University(Base):
    id=Column(String(36), primary_key=True, default=lambda:str(uuid4()))
    name=Column(String(200), nullable=False)

class Document(Base):
     
     __tablename__ = 'documents'

     id = Column(Integer, primary_key=True)
     title = Column(String(255), nullable=False)
     filename = Column(String(255), nullable=False)
     file_path = Column(String(255), nullable=False)
     file_type = Column(String(50))
     file_size = Column(BigInteger)
     upload_date = Column(DateTime, default=datetime.utcnow)
     uploaded_by = Column(Integer, ForeignKey('users.id'))
     version = Column(Integer, default=1)
     description = Column(Text)

     #Relationships
     uploader = relationship('User', back_populates='documents')
     audits = relationship('Audit', back_populates='document')
     tags = relationship('Tag', secondary='document_tag', back_populates='documents')
     permissions = relationship('Permission', back_populates='document')

class Tag(Base):

    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    # Relationships
    documents = relationship('Document', secondary='document_tag', back_populates='tags')


class DocumentTag(Base):

    __tablename__ = 'document_tag'

    document_id = Column(Integer, ForeignKey('documents.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)

class Audit(Base):

    __tablename__ = 'audit'

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('documents.id'))
    action = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    performed_by = Column(Integer, ForeignKey('users.id'))
    details = Column(Text)

    # Relationships
    document = relationship('Document', back_populates='audits')
    user = relationship('User', back_populates='audits')

class Permission(Base):

    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('documents.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    access_level = Column(String(50), nullable=False)

    # Relationships
    document = relationship('Document', back_populates='permissions')
    user = relationship('User', back_populates='permissions')
