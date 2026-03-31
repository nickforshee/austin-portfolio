import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import bcrypt

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'portfolio.db')


def resolve_database_url():
    raw_url = os.getenv('DATABASE_URL', '').strip()
    if not raw_url:
        return f'sqlite:///{DB_PATH}'

    # Support provider URLs like postgres://... and upgrade to psycopg driver.
    if raw_url.startswith('postgres://'):
        return raw_url.replace('postgres://', 'postgresql+psycopg://', 1)
    if raw_url.startswith('postgresql://'):
        return raw_url.replace('postgresql://', 'postgresql+psycopg://', 1)
    return raw_url


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = resolve_database_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'replace-this-with-a-long-secret-key-12345')
app.config['ADMIN_USERNAME'] = os.getenv('ADMIN_USERNAME', 'austin')
app.config['ADMIN_PASSWORD'] = os.getenv('ADMIN_PASSWORD', 'change-me')
app.config['PORT'] = int(os.getenv('PORT', '5000'))

cors_origins_raw = os.getenv(
    'CORS_ORIGINS',
    'http://localhost:5173,http://127.0.0.1:5173,http://localhost:4173,http://127.0.0.1:4173',
)
cors_origins = [origin.strip() for origin in cors_origins_raw.split(',') if origin.strip()]

CORS(app, resources={r'/api/*': {'origins': cors_origins}})
db = SQLAlchemy(app)
jwt = JWTManager(app)

SECTION_VALUES = {'shows', 'accomplishments', 'work', 'blog', 'gallery'}


class AdminUser(db.Model):
    __tablename__ = 'admin_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)


class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text, nullable=False)
    program_statement = db.Column(db.Text, nullable=False)
    hero_image_url = db.Column(db.String(500), nullable=True)
    email = db.Column(db.String(255), nullable=True)


class ContentItem(db.Model):
    __tablename__ = 'content_items'

    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(40), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    subtitle = db.Column(db.String(255), nullable=True)
    summary = db.Column(db.Text, nullable=True)
    body = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    external_url = db.Column(db.String(500), nullable=True)
    event_date = db.Column(db.String(40), nullable=True)
    tags = db.Column(db.String(255), nullable=True)
    published = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


def serialize_profile(row):
    return {
        'fullName': row.full_name,
        'title': row.title,
        'bio': row.bio,
        'programStatement': row.program_statement,
        'heroImageUrl': row.hero_image_url,
        'email': row.email,
    }


def serialize_item(row):
    return {
        'id': row.id,
        'section': row.section,
        'title': row.title,
        'subtitle': row.subtitle,
        'summary': row.summary,
        'body': row.body,
        'imageUrl': row.image_url,
        'externalUrl': row.external_url,
        'eventDate': row.event_date,
        'tags': row.tags,
        'published': row.published,
        'createdAt': row.created_at.isoformat() if row.created_at else None,
        'updatedAt': row.updated_at.isoformat() if row.updated_at else None,
    }


def apply_item_payload(row, payload):
    section = payload.get('section', row.section)
    if section not in SECTION_VALUES:
        raise ValueError('Invalid section')

    row.section = section
    row.title = (payload.get('title') or row.title or '').strip()
    row.subtitle = payload.get('subtitle')
    row.summary = payload.get('summary')
    row.body = payload.get('body')
    row.image_url = payload.get('imageUrl')
    row.external_url = payload.get('externalUrl')
    row.event_date = payload.get('eventDate')
    row.tags = payload.get('tags')
    row.published = bool(payload.get('published', row.published))

    if not row.title:
        raise ValueError('Title is required')


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'ok': True})


@app.route('/api/auth/login', methods=['POST'])
def login():
    payload = request.get_json(silent=True) or {}
    username = (payload.get('username') or '').strip()
    password = payload.get('password') or ''

    user = AdminUser.query.filter_by(username=username).first()
    if not user or not bcrypt.verify(password, user.password_hash):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({'accessToken': token})


@app.route('/api/profile', methods=['GET'])
def get_profile():
    row = Profile.query.first()
    if not row:
        return jsonify({'error': 'Profile not found'}), 404
    return jsonify(serialize_profile(row))


@app.route('/api/admin/profile', methods=['PUT'])
@jwt_required()
def upsert_profile():
    _user_id = get_jwt_identity()
    payload = request.get_json(silent=True) or {}

    row = Profile.query.first()
    if not row:
        row = Profile()
        db.session.add(row)

    row.full_name = (payload.get('fullName') or '').strip()
    row.title = (payload.get('title') or '').strip()
    row.bio = (payload.get('bio') or '').strip()
    row.program_statement = (payload.get('programStatement') or '').strip()
    row.hero_image_url = payload.get('heroImageUrl')
    row.email = payload.get('email')

    if not row.full_name or not row.title or not row.bio or not row.program_statement:
        return jsonify({'error': 'fullName, title, bio, and programStatement are required'}), 400

    db.session.commit()
    return jsonify(serialize_profile(row))


@app.route('/api/content/<section>', methods=['GET'])
def public_items(section):
    if section not in SECTION_VALUES:
        return jsonify({'error': 'Unknown section'}), 404

    rows = (
        ContentItem.query.filter_by(section=section, published=True)
        .order_by(ContentItem.event_date.desc().nullslast(), ContentItem.created_at.desc())
        .all()
    )
    return jsonify([serialize_item(row) for row in rows])


@app.route('/api/admin/content', methods=['GET'])
@jwt_required()
def admin_items():
    section = request.args.get('section', '').strip()
    query = ContentItem.query
    if section:
        if section not in SECTION_VALUES:
            return jsonify({'error': 'Unknown section'}), 404
        query = query.filter_by(section=section)

    rows = query.order_by(ContentItem.created_at.desc()).all()
    return jsonify([serialize_item(row) for row in rows])


@app.route('/api/admin/content', methods=['POST'])
@jwt_required()
def create_item():
    payload = request.get_json(silent=True) or {}
    row = ContentItem()
    try:
        apply_item_payload(row, payload)
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

    db.session.add(row)
    db.session.commit()
    return jsonify(serialize_item(row)), 201


@app.route('/api/admin/content/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_item(item_id):
    payload = request.get_json(silent=True) or {}
    row = ContentItem.query.get_or_404(item_id)

    try:
        apply_item_payload(row, payload)
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

    db.session.commit()
    return jsonify(serialize_item(row))


@app.route('/api/admin/content/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    row = ContentItem.query.get_or_404(item_id)
    db.session.delete(row)
    db.session.commit()
    return jsonify({'deleted': True})


def seed_data():
    if not AdminUser.query.first():
        admin = AdminUser(
            username=app.config['ADMIN_USERNAME'],
            password_hash=bcrypt.hash(app.config['ADMIN_PASSWORD']),
        )
        db.session.add(admin)

    if not Profile.query.first():
        profile = Profile(
            full_name='Austin Kimbell',
            title='Theatre Educator and Director',
            bio='Austin Kimbell is a theatre teacher focused on student-centered production design, collaborative rehearsal processes, and equitable arts access.',
            program_statement='My long-term goal is to deepen my pedagogy through graduate study, then bring advanced directing and curriculum methods back into public school theatre programs.',
            hero_image_url='https://images.unsplash.com/photo-1503095396549-807759245b35?auto=format&fit=crop&w=1200&q=80',
            email='austin@example.com',
        )
        db.session.add(profile)

    if not ContentItem.query.first():
        starter_rows = [
            ContentItem(
                section='shows',
                title='Our Town',
                subtitle='Director • 2025',
                summary='Led an ensemble-first production with student dramaturgy teams and peer feedback loops.',
                event_date='2025-11-10',
                image_url='https://images.unsplash.com/photo-1507924538820-ede94a04019d?auto=format&fit=crop&w=900&q=80',
                published=True,
            ),
            ContentItem(
                section='accomplishments',
                title='District Arts Leadership Award',
                subtitle='Recipient • 2024',
                summary='Recognized for building inclusive performance opportunities and expanding after-school participation.',
                event_date='2024-05-18',
                published=True,
            ),
            ContentItem(
                section='work',
                title='Student Devised Theatre Unit',
                subtitle='Curriculum Design',
                summary='Six-week unit blending movement, writing, and scene composition for mixed-experience students.',
                external_url='https://example.com/devised-theatre-unit',
                published=True,
            ),
            ContentItem(
                section='blog',
                title='Why Reflection Belongs in Every Rehearsal',
                subtitle='Teaching Notes',
                summary='A practical framework for critique circles that builds confidence without flattening creativity.',
                body='After each rehearsal block, students complete one warm feedback and one challenge feedback note...',
                event_date='2026-01-14',
                published=True,
            ),
            ContentItem(
                section='gallery',
                title='Spring Showcase Backstage',
                subtitle='Photo Story',
                summary='Students preparing costumes and cue sheets before curtain.',
                image_url='https://images.unsplash.com/photo-1460723237483-7a6dc9d0b212?auto=format&fit=crop&w=900&q=80',
                published=True,
            ),
        ]
        db.session.add_all(starter_rows)

    db.session.commit()


def init_db():
    with app.app_context():
        db.create_all()
        seed_data()


def should_auto_init_db():
    return os.getenv('AUTO_INIT_DB', 'true').strip().lower() in {'1', 'true', 'yes', 'on'}


if should_auto_init_db():
    init_db()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config['PORT'], debug=True)
