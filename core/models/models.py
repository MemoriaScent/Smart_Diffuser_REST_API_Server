# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Enum, Float, ForeignKey, String, Text, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Cartridge(Base):
    __tablename__ = 'Cartridge'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(25), nullable=False)
    description = Column(String(500), nullable=False)


class Creator(Base):
    __tablename__ = 'Creator'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(50), nullable=False, server_default="''")
    description = Column(String(500), nullable=False, server_default="''")
    latitude = Column(Float(asdecimal=True), nullable=False, server_default="0")
    longitude = Column(Float(asdecimal=True), nullable=False, server_default="0")
    address = Column(String(250), nullable=False, server_default="''")


class Perfume(Base):
    __tablename__ = 'Perfume'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(25), nullable=False, server_default="''")
    division = Column(String(50), nullable=False, server_default="''")
    company = Column(String(50), nullable=False, server_default="''")


class TagInfo(Base):
    __tablename__ = 'Tag_info'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(10), nullable=False, unique=True)


class User(Base):
    __tablename__ = 'User'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(25), nullable=False, server_default="''")
    image_url = Column(Text, nullable=False)
    birth = Column(Date, nullable=False)
    sex = Column(Enum('M', 'F'), nullable=False, server_default="'M'")


class CartridgeKeynote(Base):
    __tablename__ = 'Cartridge_keynote'

    id = Column(INTEGER(11), primary_key=True)
    perfume_id = Column(ForeignKey('Perfume.id'), nullable=False, index=True)
    cartridge_id = Column(ForeignKey('Cartridge.id'), nullable=False, index=True)

    cartridge = relationship('Cartridge')
    perfume = relationship('Perfume')


class CartridgeModifier(Base):
    __tablename__ = 'Cartridge_modifier'

    id = Column(INTEGER(11), primary_key=True)
    perfume_id = Column(ForeignKey('Perfume.id'), index=True)
    cartridge_id = Column(ForeignKey('Cartridge.id'), index=True)

    cartridge = relationship('Cartridge')
    perfume = relationship('Perfume')


class SetInfo(Base):
    __tablename__ = 'Set_Info'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(25), nullable=False)
    description = Column(String(500), nullable=False)
    image_url = Column(Text)
    creator = Column(ForeignKey('Creator.id'), nullable=False, index=True)
    cost = Column(INTEGER(11), nullable=False)

    Creator = relationship('Creator')


class Set(Base):
    __tablename__ = 'Set'

    id = Column(INTEGER(11), primary_key=True)
    set_id = Column(ForeignKey('Set_Info.id'), index=True)
    cartridge_id = Column(ForeignKey('Cartridge.id'), nullable=False, index=True)

    cartridge = relationship('Cartridge')
    set = relationship('SetInfo')


class UserRecipe(Base):
    __tablename__ = 'User_recipe'

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(ForeignKey('User.id'), nullable=False, index=True)
    set_id = Column(ForeignKey('Set_Info.id'), index=True)
    title = Column(String(25), nullable=False, server_default="''")
    description = Column(Text, nullable=False)
    image_url = Column(Text)
    create_time = Column(DateTime, nullable=False)

    set = relationship('SetInfo')
    user = relationship('User')


class Share(Base):
    __tablename__ = 'Share'

    id = Column(INTEGER(11), primary_key=True)
    recipe_id = Column(ForeignKey('User_recipe.id'), nullable=False, index=True)
    user_id = Column(ForeignKey('User.id'), nullable=False, index=True)

    recipe = relationship('UserRecipe')
    user = relationship('User')


class Tag(Base):
    __tablename__ = 'Tag'

    id = Column(INTEGER(11), primary_key=True)
    recipe_id = Column(ForeignKey('User_recipe.id'), nullable=False, index=True, server_default="0")
    tag_id = Column(ForeignKey('Tag_info.id'), nullable=False, index=True, server_default="0")

    recipe = relationship('UserRecipe')
    tag = relationship('TagInfo')


class UserRecipeUsePerfume(Base):
    __tablename__ = 'User_recipe_use_perfume'

    id = Column(INTEGER(11), primary_key=True)
    recipe_id = Column(ForeignKey('User_recipe.id'), nullable=False, index=True)
    cartridge_id = Column(ForeignKey('Cartridge.id'), nullable=False, index=True)
    count = Column(INTEGER(11), nullable=False)

    cartridge = relationship('Cartridge')
    recipe = relationship('UserRecipe')
