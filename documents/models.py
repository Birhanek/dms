from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_login import UserMixin
from . import Base

class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True)
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
