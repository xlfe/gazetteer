from google.appengine.api import datastore
def create_foreign_key(kind, key_is_id=False):
  def generate_foreign_key_lambda(value):
    if value is None:
      return None

    if key_is_id:
      value = int(value)
    return datastore.Key.from_path(kind, value)

  return generate_foreign_key_lambda