from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings


class Station(models.Model):
    name = models.CharField(max_length=255)
    station_id = models.CharField(max_length=255)


class DogmaAttribute(models.Model):
    attribute_id = models.IntegerField()
    value = models.FloatField()


class Station(models.Model):
    system_id = models.IntegerField()
    name = models.CharField(max_length=128)
    def get_station(station_id, esi):
        try:
            station = Station.objects.get(id=station_id)
        except:
            station = None

        if not station:
            station_data = esi.client.Universe.get_universe_stations_station_id(station_id=station_id).results()
            if station_data:
                station = Station(id=station_data['station_id'],
                                  system_id=station_data['system_id'],
                                  name=station_data['name'])
                station.save()

        return station


class Item(models.Model):
    location_id = models.IntegerField()
    type_id = models.IntegerField()
    name = models.CharField(max_length=128)
    custom_name = models.CharField(max_length=128)
    location_flag = models.CharField(max_length=128)
    location_type = models.CharField(max_length=128)
    mutator_type_id = models.IntegerField(default=-1)
    source_type_id = models.IntegerField(default=-1)
    price = models.IntegerField(default=-1)
    character = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    attributes = models.ManyToManyField(DogmaAttribute)

    def get_location_string(self, esi):
        loc = 'Unknown'
        loc_type = self.location_type

        if loc_type == 'item':
            item = Item.objects.get(id=self.location_id)
            loc = '{} ({}) - {}'.format(ItemType.objects.get(type_id=item.type_id).name, item.custom_name, item.get_location_string(esi))
        elif loc_type == 'station':
            station = Station.get_station(self.location_id, esi)
            loc = '{}'.format(station.name)
        else:
            print('Unknown location_type {}'.format(loc_type))
        return loc


class ItemType(models.Model):
    type_id = models.IntegerField()
    name = models.CharField(max_length=255)
    icon_id = models.IntegerField()
    group_id = models.IntegerField()


class AttributeType(models.Model):
    attr_id = models.IntegerField()
    name = models.CharField(max_length=255)
    displayName = models.CharField(max_length=255)







