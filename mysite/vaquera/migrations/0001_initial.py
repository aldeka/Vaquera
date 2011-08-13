# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Vaquerita'
        db.create_table('vaquera_vaquerita', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('is_maintainer', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('vaquera', ['Vaquerita'])

        # Adding model 'Issue'
        db.create_table('vaquera_issue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vaquera.Vaquerita'], null=True, blank=True)),
            ('priority', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('status', self.gf('django.db.models.fields.CharField')(default='unr', max_length=3)),
            ('milestone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vaquera.Milestone'], null=True, blank=True)),
        ))
        db.send_create_signal('vaquera', ['Issue'])

        # Adding M2M table for field tags on 'Issue'
        db.create_table('vaquera_issue_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('issue', models.ForeignKey(orm['vaquera.issue'], null=False)),
            ('tag', models.ForeignKey(orm['vaquera.tag'], null=False))
        ))
        db.create_unique('vaquera_issue_tags', ['issue_id', 'tag_id'])

        # Adding M2M table for field also_see on 'Issue'
        db.create_table('vaquera_issue_also_see', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_issue', models.ForeignKey(orm['vaquera.issue'], null=False)),
            ('to_issue', models.ForeignKey(orm['vaquera.issue'], null=False))
        ))
        db.create_unique('vaquera_issue_also_see', ['from_issue_id', 'to_issue_id'])

        # Adding model 'HistoryItem'
        db.create_table('vaquera_historyitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vaquera.Issue'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vaquera.Vaquerita'], null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('change_type', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('change_description', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('vaquera', ['HistoryItem'])

        # Adding model 'FileUpload'
        db.create_table('vaquera_fileupload', (
            ('historyitem_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['vaquera.HistoryItem'], unique=True, primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('vaquera', ['FileUpload'])

        # Adding model 'Comment'
        db.create_table('vaquera_comment', (
            ('historyitem_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['vaquera.HistoryItem'], unique=True, primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('vaquera', ['Comment'])

        # Adding model 'Tag'
        db.create_table('vaquera_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('vaquera', ['Tag'])

        # Adding model 'Milestone'
        db.create_table('vaquera_milestone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('start_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('vaquera', ['Milestone'])


    def backwards(self, orm):
        
        # Deleting model 'Vaquerita'
        db.delete_table('vaquera_vaquerita')

        # Deleting model 'Issue'
        db.delete_table('vaquera_issue')

        # Removing M2M table for field tags on 'Issue'
        db.delete_table('vaquera_issue_tags')

        # Removing M2M table for field also_see on 'Issue'
        db.delete_table('vaquera_issue_also_see')

        # Deleting model 'HistoryItem'
        db.delete_table('vaquera_historyitem')

        # Deleting model 'FileUpload'
        db.delete_table('vaquera_fileupload')

        # Deleting model 'Comment'
        db.delete_table('vaquera_comment')

        # Deleting model 'Tag'
        db.delete_table('vaquera_tag')

        # Deleting model 'Milestone'
        db.delete_table('vaquera_milestone')


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
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vaquera.Vaquerita']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'milestone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vaquera.Milestone']", 'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'unr'", 'max_length': '3'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['vaquera.Tag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'vaquera.milestone': {
            'Meta': {'object_name': 'Milestone'},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'start_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'vaquera.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'vaquera.vaquerita': {
            'Meta': {'object_name': 'Vaquerita', '_ormbases': ['auth.User']},
            'is_maintainer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['vaquera']
