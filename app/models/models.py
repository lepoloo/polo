from sqlalchemy import Enum,Column, Integer, String, Double, TIMESTAMP, Date, Boolean, DateTime, text,ForeignKey,ARRAY
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

######################## User #############################
class GenderType(enum.Enum):
    M = 1
    F = 2
    
# User : doing
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String, index=True , unique=True, nullable=False)
    birthday = Column(String, nullable=False)
    gender = Column(Enum(GenderType), nullable=False, default="M")
    email = Column(String, index=True, unique=True, nullable=False)
    image = Column(String, index=True, unique=True, nullable=False)
    username = Column(String, index=True, unique=True, nullable=False)
    password = Column(String(length=256), index=True)
    is_staff = Column(Boolean, default=False)
    is_owner = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    
    # Colonnes étrangères inversées
    entertainment_sites = relationship("EntertainmentSite", back_populates="owner")
    profils = relationship("Profil", back_populates="owner")
    notes = relationship("Note", back_populates="owner")
    favorites = relationship("Favorite", back_populates="owner")
    
    

# Role : doing
class Role(Base):
    __tablename__ = "roles"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String(length=65535), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    
    # Colonnes étrangères inversées
    profil_roles = relationship("ProfilRole", back_populates="role")
    privilege_roles = relationship("PrivilegeRole", back_populates="role")
 
# Privilege : doing   
class Privilege(Base):
    __tablename__ = "privileges"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String(length=65535), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    
    # Colonnes étrangères inversées
    privilege_roles = relationship("PrivilegeRole", back_populates="privilege")
    profil_privileges = relationship("ProfilPrivilege", back_populates="privilege")

# Privilege_role : doing   
class PrivilegeRole(Base):
    __tablename__ = "privilege_roles"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    
    role_id = Column(String, ForeignKey(
        "roles.id", ondelete="CASCADE"), nullable=False)
    role = relationship("Role", back_populates="privilege_roles")
    privilege_id = Column(String, ForeignKey(
        "privileges.id", ondelete="CASCADE"), nullable=False)
    privilege = relationship("Privilege", back_populates="privilege_roles")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    
# Profil : doing   
class Profil(Base):
    __tablename__ = "profils"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    fucntion = Column(String, index=True, nullable=False)
    description = Column(String(length=65535), nullable=True)
    
    owner_id = Column(String, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="profils")
    
    
    entertainment_sites_id = Column(String, ForeignKey(
        "entertainment_sites.id", ondelete="CASCADE"), nullable=False)
    entertainment_site = relationship("EntertainmentSite", back_populates="profils")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    
    # Colonnes étrangères inversées countryId
    profil_roles = relationship("ProfilRole", back_populates="profil")
    profil_privileges = relationship("ProfilPrivilege", back_populates="profil")
    
# ProfilRole : to do   
class ProfilRole(Base):
    __tablename__ = "profil_roles"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    
    profil_id = Column(String, ForeignKey(
        "profils.id", ondelete="CASCADE"), nullable=False)
    profil = relationship("Profil", back_populates="profil_roles")
    role_id = Column(String, ForeignKey(
        "roles.id", ondelete="CASCADE"), nullable=False)
    role = relationship("Role", back_populates="profil_roles")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    
    # Colonnes étrangères inversées
    profil = relationship("Profil", back_populates="profil_roles")
    
    
# ProfilPrivilege : to do   
class ProfilPrivilege(Base):
    __tablename__ = "profil_privileges"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    
    profil_id = Column(String, ForeignKey(
        "profils.id", ondelete="CASCADE"), nullable=False)
    profil = relationship("Profil", back_populates="profil_privileges")
    privilege_id = Column(String, ForeignKey(
        "privileges.id", ondelete="CASCADE"), nullable=False)
    privilege = relationship("Privilege", back_populates="profil_privileges")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    
    # Colonnes étrangères inversées
    profil = relationship("Profil", back_populates="profil_privileges")
    

    ######################## Card #############################
    
   
# FamilyCard : doing    
class FamilyCard(Base):
    __tablename__ = "family_cards"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String(length=65535), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    # Colonnes étrangères inversées
    cards = relationship("Card", back_populates="family_card")


# Card : doing  
class Card(Base):
    __tablename__ = "cards"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    multimedia = Column(String, nullable=False)
    description = Column(String(length=65535), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    # relationship
    family_card_id = Column(String, ForeignKey(
        "family_cards.id", ondelete="CASCADE"), nullable=False)
    family_card = relationship("FamilyCard", back_populates="cards")
    entertainment_site_id = Column(String, ForeignKey(
        "entertainment_sites.id", ondelete="CASCADE"), nullable=False)
    entertainment_site = relationship("EntertainmentSite", back_populates="cards")
    # Colonnes étrangères inversées
    menus = relationship("Menu", back_populates="card")

    
    
# TypeProduct : doing   
class TypeProduct(Base):
    __tablename__ = "type_products"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String(length=65535), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    
    # Colonnes étrangères inversées
    products = relationship("Product", back_populates="type_product")
    
# Product : doing     
class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String(length=65535), nullable=False)
    price = Column(Double, nullable=True)
    image = Column(String, index=True, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    # relationship
    type_product_id = Column(String, ForeignKey(
        "type_products.id", ondelete="CASCADE"), nullable=False)
    type_product = relationship("TypeProduct", back_populates="products")
    # Colonnes étrangères inversées
    menus = relationship("Menu", back_populates="product")
    
# Menu : doing    
class Menu(Base):
    __tablename__ = "menus"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    price = Column(Double, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    # relationship
    product_id = Column(String, ForeignKey(
        "products.id", ondelete="CASCADE"), nullable=False)
    product = relationship("Product", back_populates="menus")
    
    card_id = Column(String, ForeignKey(
        "cards.id", ondelete="CASCADE"), nullable=False)
    card = relationship("Card", back_populates="menus")
    
    
    
################## Entertement Site ################################

# Country : doing 
class Country(Base):
    __tablename__ = "contries"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    
    # Colonnes étrangères inversées
    towns = relationship("Town", back_populates="country")

# Town : doing  
class Town(Base):
    __tablename__ = "towns"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    
    country_id = Column(String, ForeignKey(
        "contries.id", ondelete="CASCADE"), nullable=False)
    country = relationship("Country", back_populates="towns")
    
    # Colonnes étrangères inversées
    quaters = relationship("Quarter", back_populates="town")

# Quarter : doing  
class Quarter(Base):
    __tablename__ = "quarters"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    
    town_id = Column(String, ForeignKey(
        "towns.id", ondelete="CASCADE"), nullable=False)
    town = relationship("Town", back_populates="quaters")
    
    # Colonnes étrangères inversées countryId
    entertainment_sites = relationship("EntertainmentSite", back_populates="quarter")

# CategorySite : doing
class CategorySite(Base):
    __tablename__ = "category_sites"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String(length=65535), nullable=False)
    image = Column(String, index=True, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    
    # Colonnes étrangères inversées
    entertainment_sites = relationship("EntertainmentSite", back_populates="category_site")
 
# Reservation : doing
class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    date = Column(DateTime)
    nb_personne = Column(Integer, nullable=False)
    hour = Column(String, nullable=False)
    description = Column(String(length=65535), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    entertainment_site_id = Column(String, ForeignKey(
        "entertainment_sites.id", ondelete="CASCADE"), nullable=False)
    entertainment_site = relationship("EntertainmentSite", back_populates="reservations")
    
 
 
# Comment : doing
class Comment(Base):
    __tablename__ = "comments"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    content = Column(String(length=65535), nullable=True)
    note = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    entertainment_site_id = Column(String, ForeignKey(
        "entertainment_sites.id", ondelete="CASCADE"), nullable=False)
    entertainment_site = relationship("EntertainmentSite", back_populates="comments")
    
    
 
# Program : doing
class Program(Base):
    __tablename__ = "programs"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    description = Column(String(length=65535), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    entertainment_site_id = Column(String, ForeignKey(
        "entertainment_sites.id", ondelete="CASCADE"), nullable=False)
    entertainment_site = relationship("EntertainmentSite", back_populates="programs")
    
    # Colonnes étrangères inversées
    schedule_time = relationship("ScheduleTime", back_populates="programs")
 

 
# Program : doing
class ScheduleTime(Base):
    __tablename__ = "schedule_times"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    daily_day = Column(String, unique=True, nullable=False)
    open_hour = Column(String, unique=True, nullable=False)
    close_hour = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    program_id = Column(String, ForeignKey(
        "programs.id", ondelete="CASCADE"), nullable=False)
    programs = relationship("Program", back_populates="schedule_time")
    
 
 
 
# EntertainmentSite : doing 
class EntertainmentSite(Base):
    __tablename__ = "entertainment_sites"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String(length=65535), nullable=True)
    nb_visite = Column(Integer,default=None, nullable=True)
    address = Column(String, unique=True, nullable=False)
    longitude = Column(String, unique=True, nullable=False)
    latitude = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    # images = Column(ARRAY(String))
    
    owner_id = Column(String, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="entertainment_sites")
    
    quarter_id = Column(String, ForeignKey(
        "quarters.id", ondelete="CASCADE"), nullable=False)
    quarter = relationship("Quarter", back_populates="entertainment_sites")
    
    category_site_id = Column(String, ForeignKey(
        "category_sites.id", ondelete="CASCADE"), nullable=False)
    category_site = relationship("CategorySite", back_populates="entertainment_sites")
    
    # Colonnes étrangères inversées countryId
    cards = relationship("Card", back_populates="entertainment_site")
    reservations = relationship("Reservation", back_populates="entertainment_site")
    comments = relationship("Comment", back_populates="entertainment_site")
    programs = relationship("Program", back_populates="entertainment_site")
    anounces = relationship("Anounce", back_populates="entertainment_site")
    events = relationship("Event", back_populates="entertainment_site")
    profils = relationship("Profil", back_populates="entertainment_site")
    entertainment_site_multimedias = relationship("EntertainmentSiteMultimedia", back_populates="entertainment_site")
    notes = relationship("Note", back_populates="entertainment_site")
    favorites = relationship("Favorite", back_populates="entertainment_site")

    
    ###################### Anounce #########################  

# Anounce : doing
class Anounce(Base):
    __tablename__ = "anounces"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    nb_visite = Column(Integer,default=None, nullable=True)
    description = Column(String(length=65535), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    entertainment_site_id = Column(String, ForeignKey(
        "entertainment_sites.id", ondelete="CASCADE"), nullable=False)
    entertainment_site = relationship("EntertainmentSite", back_populates="anounces")
    
    # Colonnes étrangères inversées
    anounce_multimedias = relationship("AnounceMultimedia", back_populates="anounce")
    
     
# Event : doing
class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    description = Column(String(length=65535), nullable=True)
    nb_visite = Column(Integer,default=None, nullable=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    start_hour = Column(String, nullable=False)
    end_hour = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    entertainment_site_id = Column(String, ForeignKey(
        "entertainment_sites.id", ondelete="CASCADE"), nullable=False)
    entertainment_site = relationship("EntertainmentSite", back_populates="events")
    label_event_id = Column(String, ForeignKey(
        "label_events.id", ondelete="CASCADE"), nullable=False)
    label_event = relationship("LabelEvent", back_populates="events")
    
    # Colonnes étrangères inversées
    event_multimedias = relationship("EventMultimedia", back_populates="event")
    
    
# LabelEvent : doing   
class LabelEvent(Base):
    __tablename__ = "label_events"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String(length=65535), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    
    # Colonnes étrangères inversées
    events = relationship("Event", back_populates="label_event")
    

# AnounceMultimedia : to doing    
class AnounceMultimedia(Base):
    __tablename__ = "anounce_multimedias"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    link_media = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    # relationship
    anounce_id = Column(String, ForeignKey(
        "anounces.id", ondelete="CASCADE"), nullable=False)
    anounce = relationship("Anounce", back_populates="anounce_multimedias")

# EvenMultimedia : to doing    
class EventMultimedia(Base):
    __tablename__ = "event_multimedias"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    link_media = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    # relationship
    event_id = Column(String, ForeignKey(
        "events.id", ondelete="CASCADE"), nullable=False)
    event = relationship("Event", back_populates="event_multimedias")

# AnounceMultimedia : to doing    
class EntertainmentSiteMultimedia(Base):
    __tablename__ = "entertainment_site_multimedias"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    link_media = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    # relationship
    entertainment_site_id = Column(String, ForeignKey(
        "entertainment_sites.id", ondelete="CASCADE"), nullable=False)
    entertainment_site = relationship("EntertainmentSite", back_populates="entertainment_site_multimedias")
    
    
    ###################### Note and Favorites #########################  

# Note : doing
class Note(Base):
    __tablename__ = "notes"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    note = Column(Double,default=None, nullable=True)
    owner_id = Column(String, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="notes")
    entertainment_site_id = Column(String, ForeignKey(
        "entertainment_sites.id", ondelete="CASCADE"), nullable=False)
    entertainment_site = relationship("EntertainmentSite", back_populates="notes")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)

# Anounce : doing
class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    refnumber = Column(String, unique=True, nullable=False)
    owner_id = Column(String, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="favorites")
    entertainment_site_id = Column(String, ForeignKey(
        "entertainment_sites.id", ondelete="CASCADE"), nullable=False)
    entertainment_site = relationship("EntertainmentSite", back_populates="favorites")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    active = Column(Boolean, default=True)