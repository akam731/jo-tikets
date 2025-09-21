# Generated manually to remove unique constraint

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0002_alter_cartitem_unique_together"),
    ]

    operations = [
        migrations.RunSQL(
            "DROP INDEX IF EXISTS cart_cartitem_cart_id_offer_id_uniq;",
            reverse_sql="CREATE UNIQUE INDEX cart_cartitem_cart_id_offer_id_uniq ON cart_cartitem (cart_id, offer_id);",
        ),
    ]
