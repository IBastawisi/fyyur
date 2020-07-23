from config import db

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)

    venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"), nullable=False)

    venue = db.relationship("Venue", back_populates="shows")
    artist = db.relationship("Artist", back_populates="shows")

    def __repr__(self):
        return f'{self.id}: {self.name}'


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    genres = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(500))
    shows = db.relationship("Show", cascade="all,delete", back_populates="venue")

    def __repr__(self):
        return f'{self.id}: {self.name}'


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(500))
    shows = db.relationship("Show", cascade="all,delete", back_populates="artist")

    def __repr__(self):
        return f'{self.id}: {self.name}'