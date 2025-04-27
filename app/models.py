from . import db

class ArrInstance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    arr_type = db.Column(db.String(20), nullable=False)  # 'radarr', 'sonarr', etc.
    url = db.Column(db.String(255), nullable=False)
    api_key = db.Column(db.String(255), nullable=False)
    sync_interval = db.Column(db.Integer, default=3600)  # seconds

class UnmonitorRule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    arr_instance_id = db.Column(db.Integer, db.ForeignKey('arr_instance.id'), nullable=False)
    quality_profile = db.Column(db.String(120), nullable=False)
    release_groups = db.Column(db.Text, nullable=False)  # JSON array of groups
    media_type = db.Column(db.String(20))  # 'movie', 'series', 'episode', etc.