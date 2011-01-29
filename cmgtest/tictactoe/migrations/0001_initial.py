# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TTTSession'
        db.create_table('tictactoe_tttsession', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('board', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('tictactoe', ['TTTSession'])


    def backwards(self, orm):
        
        # Deleting model 'TTTSession'
        db.delete_table('tictactoe_tttsession')


    models = {
        'tictactoe.tttsession': {
            'Meta': {'object_name': 'TTTSession'},
            'board': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['tictactoe']
