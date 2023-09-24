# """
# automatic database routing scheme
# """

# # credits: Akuya Ekorot [Backend Engineer]

# class PrimaryRouter:
#     """A router to control all database operations on models in hngx application
#     """
    
#     def db_for_read(self, model, **hints):
#         """Suggest the database that should be used for
#            read operations for objects of type model,
#            Else:
#                 return None
#         """
#         return 'primary'
    
#     def db_for_write(self, model, **hints):
#         """Suggest the database that should be used for
#            write operations for objects of type model,
#            Else:
#                 return None
#         """
#         return 'primary'
    
#     def allow_relation(self, obj1, obj2, **hints):
#         """Return True:
#                 if a relation between obj1 and obj2 should be allowed
#            False:
#                 if the relation should be prevented, or
#            None:
#                 if the router has no opinion
#         """
#         return True
    
#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         """Determine if the migration operation is allowed to run on the database with alias db.
        
#            Return True:
#                 if the operation should run
#            False:
#                 if it shouldn't run, or
#             None:
#                 if the router has no opinion.
#         """
#         return False
    

# class DefaultRouter:
#     """A router to control all database operations on models in
#        the auth and contenttypes application
#     """
    
#     route_app_labels = {"auth", "contenttypes", "admin", "sessions", "messages",
#                         "staticfiles", "django_celery_beat", "myapp.apps.MyappConfig",
#                         "rest_framework", 'drf_yasg', 'rest_framework.authtoken', 'social_django',}
    
#     def db_for_read(self, model, **hints):
#         """
#         Attempts to read auth and contenttypes models go to auth_db.
#         """
#         if model._meta.app_label in self.route_app_labels:
#             return "default"

#     def db_for_write(self, model, **hints):
#         """
#         Attempts to write auth and contenttypes models go to auth_db.
#         """
#         if model._meta.app_label in self.route_app_labels:
#             return "defalt"

#     def allow_relation(self, obj1, obj2, **hints):
#         """
#         Allow relations if a model in the auth or contenttypes apps is
#         involved.
#         """
#         if (
#             obj1._meta.app_label in self.route_app_labels
#             or obj2._meta.app_label in self.route_app_labels
#         ):
#             return True

#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         """
#         Make sure the auth and contenttypes apps only appear in the
#         'auth_db' database.
#         """
#         if app_label in self.route_app_labels:
#             return True