# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding unique constraint on 'Tag', fields ['name']
        db.create_unique('vaquera_tag', ['name'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Tag', fields ['name']
        db.delete_unique('vaquera_tag', ['name'])


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'vaquera.comment': {
            'Meta': {'object_name': 'Comment', '_ormbases': ['vaquera.HistoryItem']},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'historyitem_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['vaquera.HistoryItem']", 'unique': 'True', 'primary_key': 'True'})
        },
        'vaquera.fileupload': {
            'Meta': {'object_name': 'FileUpload', '_ormbases': ['vaquera.HistoryItem']},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'historyitem_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['vaquera.HistoryItem']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'vaquera.historyitem': {
            'Meta': {'object_name': 'HistoryItem'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vaquera.Vaquerita']", 'null': 'True', 'blank': 'True'}),
            'change_description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'change_type': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vaquera.Issue']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'vaquera.issue': {
            'Meta': {'object_name': 'Issue'},
            'also_see': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'also_see_rel_+'", 'null': 'True', 'to': "orm['vaquera.Issue']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'authored_issue_set'", 'null': 'True', 'to': "orm['vaquera.Vaquerita']"}),
            'followers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'followed_issue_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['vaquera.Vaquerita']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'milestone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vaquera.Milestone']", 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owned_issue_set'", 'null': 'True', 'to': "orm['vaquera.Vaquerita']"}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['vaquera.Tag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'vaquera.milestone': {
            'Meta': {'ordering': "['end_date']", 'object_name': 'Milestone'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'vaquera.tag': {
            'Meta': {'ordering': "['name']", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'vaquera.vaquerita': {
            'Meta': {'ordering': "['username']", 'object_name': 'Vaquerita', '_ormbases': ['auth.User']},
            'is_maintainer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['vaquera']
