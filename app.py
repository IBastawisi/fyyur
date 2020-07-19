#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
from datetime import datetime
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
import sys
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)

    venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        "artist.id"), nullable=False)

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
    shows = db.relationship("Show", back_populates="venue")

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
    shows = db.relationship("Show", back_populates="artist")

    def __repr__(self):
        return f'{self.id}: {self.name}'


#----------------------------------------------------------------------------#
# Initial Data.
#----------------------------------------------------------------------------#
db.drop_all()
db.create_all()

artist1 = Artist(
    name="Guns N Petals",
    genres="Rock n Roll",
    city="San Francisco",
    state="CA",
    phone="326-123-5000",
    website="https://www.gunsnpetalsband.com",
    facebook_link="https://www.facebook.com/GunsNPetals",
    seeking_venue=True,
    seeking_description="Looking for shows to perform at in the San Francisco Bay Area!",
    image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
)

artist2 = Artist(
    name="Matt Quevedo",
    genres="Jazz",
    city="New York",
    state="NY",
    phone="300-400-5000",
    facebook_link="https://www.facebook.com/mattquevedo923251523",
    seeking_venue=False,
    image_link="https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
)

artist3 = Artist(
    name="The Wild Sax Band",
    genres="Jazz,Classical",
    city="San Francisco",
    state="CA",
    phone="432-325-5432",
    seeking_venue=False,
    image_link="https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
)

venue1 = Venue(
    name="The Musical Hop",
    genres="Jazz,Reggae,Swing,Classical,Folk",
    address="1015 Folsom Street",
    city="San Francisco",
    state="CA",
    phone="123-123-1234",
    website="https://www.themusicalhop.com",
    facebook_link="https://www.facebook.com/TheMusicalHop",
    seeking_talent=True,
    seeking_description="We are on the lookout for a local artist to play every two weeks. Please call us.",
    image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
)

venue2 = Venue(
    name="The Dueling Pianos Bar",
    genres="Classical,R&B,Hip-Hop",
    address="335 Delancey Street",
    city="New York",
    state="NY",
    phone="914-003-1132",
    website="https://www.theduelingpianos.com",
    facebook_link="https://www.facebook.com/theduelingpianos",
    seeking_talent=False,
    image_link="https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
)

venue3 = Venue(
    name="Park Square Live Music & Coffee",
    genres="Rock n Roll,Jazz,Classical,Folk",
    address="34 Whiskey Moore Ave",
    city="San Francisco",
    state="CA",
    phone="415-000-1234",
    website="https://www.parksquarelivemusicandcoffee.com",
    facebook_link="https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    seeking_talent=False,
    image_link="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
)

show1 = Show(
    venue_id=1,
    artist_id=1,
    start_time="2019-05-21T21:30:00.000Z"
)

show2 = Show(
    venue_id=3,
    artist_id=2,
    start_time="2019-06-15T23:00:00.000Z"
)

show3 = Show(
    venue_id=3,
    artist_id=3,
    start_time="2035-04-01T20:00:00.000Z"
)

show4 = Show(
    venue_id=3,
    artist_id=3,
    start_time="2035-05-01T20:00:00.000Z"
)

show5 = Show(
    venue_id=3,
    artist_id=3,
    start_time="2035-06-01T20:00:00.000Z"
)

db.session.add_all([artist1, artist2, artist3, venue1, venue2,
                    venue3, show1, show2, show3, show4, show5])
db.session.commit()

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    if type(value) is str:
        date = dateutil.parser.parse(value)
    else:
        date = value

    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    areas = Venue.query.with_entities(Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()
    upcoming_shows = Show.query.with_entities(Show.venue_id, db.func.count("*").label("num_upcoming_shows")).filter(Show.start_time > datetime.today()).group_by(Show.venue_id).subquery()

    data = []
    for area in areas:
        data.append({
            "city": area.city,
            "state": area.state,
            "venues": Venue.query.filter(Venue.city==area.city).with_entities(Venue.id, Venue.name, upcoming_shows.c.num_upcoming_shows).outerjoin(upcoming_shows, upcoming_shows.c.venue_id == Venue.id).all()
        }) 

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():

    venues = Venue.query.with_entities(Venue.id, Venue.name).filter(Venue.name.ilike(
        f"%{request.form.get('search_term', '')}%")).all()

    response = {'count': len(venues), 'data': venues}

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

    venue = Venue.query.get(venue_id)
    upcoming_shows = Show.query.join(Show.artist).with_entities(Artist.id.label("artist_id"), Artist.name.label("artist_name"), Artist.image_link.label("artist_image_link"), Show.start_time).filter(
        Show.venue_id == venue_id, Show.start_time > datetime.today()).all()
    past_shows = Show.query.join(Show.artist).with_entities(Artist.id.label("artist_id"), Artist.name.label("artist_name"), Artist.image_link.label("artist_image_link"), Show.start_time).filter(
        Show.venue_id == venue_id, Show.start_time <= datetime.today()).all()

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres.split(","),
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "image_link": venue.image_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,

        "upcoming_shows": upcoming_shows,
        "past_shows": past_shows,
        "upcoming_shows_count": len(upcoming_shows),
        "past_shows_count": len(past_shows)
    }

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

    try:
        form = {**request.form}
        form['genres'] = ','.join(request.form.getlist("genres"))
        venue = Venue(**form)
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')
        abort(400)

    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():

    artists = Artist.query.with_entities(Artist.id, Artist.name).all()

    return render_template('pages/artists.html', artists=artists)


@app.route('/artists/search', methods=['POST'])
def search_artists():

    artists = Artist.query.with_entities(Artist.id, Artist.name).filter(Artist.name.ilike(
        f"%{request.form.get('search_term', '')}%")).all()

    response = {'count': len(artists), 'data': artists}

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

    artist = Artist.query.get(artist_id)
    upcoming_shows = Show.query.join(Show.venue).with_entities(Venue.id.label("venue_id"), Venue.name.label("venue_name"), Venue.image_link.label("venue_image_link"), Show.start_time).filter(
        Show.artist_id == artist_id, Show.start_time > datetime.today()).all()
    past_shows = Show.query.join(Show.venue).with_entities(Venue.id.label("venue_id"), Venue.name.label("venue_name"), Venue.image_link.label("venue_image_link"), Show.start_time).filter(
        Show.artist_id == artist_id, Show.start_time <= datetime.today()).all()

    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres.split(","),
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "image_link": artist.image_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,

        "upcoming_shows": upcoming_shows,
        "past_shows": past_shows,
        "upcoming_shows_count": len(upcoming_shows),
        "past_shows_count": len(past_shows)
    }

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@ app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(obj=artist)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@ app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

    try:
        form = {**request.form}
        form['genres'] = ','.join(request.form.getlist("genres"))
        artist = Artist.query.get(artist_id)
        for key, value in form.items():
            setattr(artist, key, value)

        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully updated!')

    except:
        db.session.rollback()
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be updated.')
        abort(400)

    finally:
        db.session.close()


    return redirect(url_for('show_artist', artist_id=artist_id))


@ app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(obj=venue)
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@ app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

    try:
        form = {**request.form}
        form['genres'] = ','.join(request.form.getlist("genres"))
        venue = Venue.query.get(venue_id)
        for key, value in form.items():
            setattr(venue, key, value)

        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully updated!')

    except:
        db.session.rollback()
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be updated.')
        abort(400)

    finally:
        db.session.close()


    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@ app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@ app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    try:
        form = {**request.form}
        form['genres'] = ','.join(request.form.getlist("genres"))
        artist = Artist(**form)
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')

    except:
        db.session.rollback()
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be listed.')
        abort(400)

    finally:
        db.session.close()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@ app.route('/shows')
def shows():
    shows = Show.query.join(Venue).join(Artist).with_entities(Show.venue_id, Show.artist_id, Show.start_time,
        Venue.name.label("venue_name"), Artist.name.label("artist_name"), Artist.image_link.label("artist_image_link")).all()
    return render_template('pages/shows.html', shows=shows)


@ app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@ app.route('/shows/create', methods=['POST'])
def create_show_submission():
    try:
        show = Show(**request.form)
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Show could not be listed.')
        abort(400)

    finally:
        db.session.close()

    return render_template('pages/home.html')


@ app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@ app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
