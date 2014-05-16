# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Account'
        db.create_table(u'core_account', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('init_balance', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=13, decimal_places=2)),
            ('balance', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=13, decimal_places=2)),
            ('creation_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='accounts', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'core', ['Account'])

        # Adding model 'BusinessSegment'
        db.create_table(u'core_businesssegment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'core', ['BusinessSegment'])

        # Adding model 'Person'
        db.create_table(u'core_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('document', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('business_segment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.BusinessSegment'])),
        ))
        db.send_create_signal(u'core', ['Person'])

        # Adding model 'Revenue'
        db.create_table(u'core_revenue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('value', self.gf('django.db.models.fields.DecimalField')(max_digits=13, decimal_places=2)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='related_revenues', to=orm['core.Account'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='revenues', to=orm['core.Person'])),
        ))
        db.send_create_signal(u'core', ['Revenue'])

        # Adding model 'Expense'
        db.create_table(u'core_expense', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('value', self.gf('django.db.models.fields.DecimalField')(max_digits=13, decimal_places=2)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='related_expenses', to=orm['core.Account'])),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(related_name='expenses', to=orm['core.Person'])),
        ))
        db.send_create_signal(u'core', ['Expense'])

        # Adding model 'TransactionEvent'
        db.create_table(u'core_transactionevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('value', self.gf('django.db.models.fields.DecimalField')(max_digits=13, decimal_places=2)),
            ('transaction_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'core', ['TransactionEvent'])

        # Adding model 'Receivable'
        db.create_table(u'core_receivable', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=13, decimal_places=2)),
            ('due_date', self.gf('django.db.models.fields.DateField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='related_receivables', to=orm['core.Account'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='receivables', to=orm['core.Person'])),
        ))
        db.send_create_signal(u'core', ['Receivable'])

        # Adding model 'Payable'
        db.create_table(u'core_payable', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=13, decimal_places=2)),
            ('due_date', self.gf('django.db.models.fields.DateField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='related_payables', to=orm['core.Account'])),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(related_name='payables', to=orm['core.Person'])),
        ))
        db.send_create_signal(u'core', ['Payable'])


    def backwards(self, orm):
        # Deleting model 'Account'
        db.delete_table(u'core_account')

        # Deleting model 'BusinessSegment'
        db.delete_table(u'core_businesssegment')

        # Deleting model 'Person'
        db.delete_table(u'core_person')

        # Deleting model 'Revenue'
        db.delete_table(u'core_revenue')

        # Deleting model 'Expense'
        db.delete_table(u'core_expense')

        # Deleting model 'TransactionEvent'
        db.delete_table(u'core_transactionevent')

        # Deleting model 'Receivable'
        db.delete_table(u'core_receivable')

        # Deleting model 'Payable'
        db.delete_table(u'core_payable')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.account': {
            'Meta': {'ordering': "['-creation_date']", 'object_name': 'Account'},
            'balance': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '13', 'decimal_places': '2'}),
            'creation_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'init_balance': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '13', 'decimal_places': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'accounts'", 'to': u"orm['auth.User']"})
        },
        u'core.businesssegment': {
            'Meta': {'object_name': 'BusinessSegment'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'core.expense': {
            'Meta': {'object_name': 'Expense'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_expenses'", 'to': u"orm['core.Account']"}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'expenses'", 'to': u"orm['core.Person']"}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '2'})
        },
        u'core.payable': {
            'Meta': {'ordering': "['due_date']", 'object_name': 'Payable'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_payables'", 'to': u"orm['core.Account']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'due_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payables'", 'to': u"orm['core.Person']"}),
            'value': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '13', 'decimal_places': '2'})
        },
        u'core.person': {
            'Meta': {'object_name': 'Person'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'business_segment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.BusinessSegment']"}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'document': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'core.receivable': {
            'Meta': {'ordering': "['due_date']", 'object_name': 'Receivable'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_receivables'", 'to': u"orm['core.Account']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'receivables'", 'to': u"orm['core.Person']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'due_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '13', 'decimal_places': '2'})
        },
        u'core.revenue': {
            'Meta': {'object_name': 'Revenue'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_revenues'", 'to': u"orm['core.Account']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'revenues'", 'to': u"orm['core.Person']"}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '2'})
        },
        u'core.transactionevent': {
            'Meta': {'object_name': 'TransactionEvent'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'transaction_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '2'})
        }
    }

    complete_apps = ['core']