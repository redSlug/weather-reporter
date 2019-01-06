import os, requests, time

from google.transit import gtfs_realtime_pb2
from dotenv import load_dotenv, find_dotenv
from protobuf_to_dict import protobuf_to_dict


MTA_URL = 'http://datamine.mta.info/mta_esi.php'
TIMES_TO_GET = 6


class TrainInfo:
    def __init__(self, api_key, feed_id, station):
        self.api_key = api_key
        self.feed_id = feed_id
        self.station = station
        self.feed_message = gtfs_realtime_pb2.FeedMessage()
        
    @staticmethod
    def get_train_time_with_label(train, arrival_time, now):
        minutes_until_train = (arrival_time - int(now)) / 60
        minutes = "{0:.1f}".format(minutes_until_train)
        return " {}: {}".format(train, minutes)

    @staticmethod
    def get_train_time(arrival_time, now):
        minutes_until_train = (arrival_time - int(now)) / 60
        return " {0:.1f}".format(minutes_until_train)

    def get_train_time_data(self, train_data):
        train_time_data = list()
        for trains in train_data:
            trip_update = trains.get('trip_update')
            if not trip_update:
                continue

            route_id = trip_update['trip']['route_id']

            stop_time_update = trip_update['stop_time_update']
            for stop_info in stop_time_update:
                if stop_info.get('stop_id') == self.station:
                    arrival = stop_info.get('arrival')
                    if not arrival:
                        continue
                    train_time_data.append((route_id, arrival['time']))
        return train_time_data

    def get_train_time_strings(self, train_time_data):
        if len(train_time_data) < 1:
            return "no times"

        train_time_data.sort(key=lambda route_time: route_time[1])

        now = time.time()

        train_output = list()

        for i, train_arrival_time in enumerate(train_time_data[:TIMES_TO_GET]):
            train, arrival_time = train_arrival_time
            minutes_until_arrival = (arrival_time - int(now)) / 60
            if minutes_until_arrival < 1:
                continue
            if i < 1 or train_time_data[i-1][0] != train:
                train_output.append(
                    self.get_train_time_with_label(train, arrival_time, now))
            else:
                train_output.append(self.get_train_time(arrival_time, now))

        return ','.join(train_output)

    def get_train_identifiers_for_all_feeds(self):
        def get_train_ids(feed_entities):
            for entity in feed_entities:
                trip_update = entity.get('trip_update')
                if not trip_update:
                    continue
                trip = trip_update['trip']
                if not trip:
                    continue
                route_id = trip.get('route_id')
                if route_id:
                    yield route_id

        possible_feed_ids = range(1, 60)

        for feed_id in possible_feed_ids:
            feed = self.get_feed(feed_id=feed_id)
            if feed:
                train_ids = ','.join(set(get_train_ids(feed)))
                yield 'feed_id={}: {}'.format(feed_id, train_ids)

    def get_train_data(self):
        feed = self.get_feed()
        train_time_data = self.get_train_time_data(feed)
        return self.get_train_time_strings(train_time_data)

    def get_feed(self, feed_id=None):
        feed_id = feed_id or self.feed_id
        query_str = '?key={}&feed_id={}'.format(
            self.api_key, feed_id
        )
        response = requests.get(MTA_URL + query_str)

        try:
            self.feed_message.ParseFromString(response.content)
            subway_feed = protobuf_to_dict(self.feed_message)
            return subway_feed['entity']
        except Exception:
            return


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    API_KEY = os.environ['API_KEY']
    FEED_IDS = os.environ['FEED_IDS'].split(',')
    STATIONS = os.environ['STOPS'].split(',')

    if False:    # TODO add flag
        for feed_id, station in zip(FEED_IDS, STATIONS):
            ti = TrainInfo(api_key=API_KEY,
                           feed_id=feed_id,
                           station=station)
            print(ti.get_train_data())
    else:
        ti = TrainInfo(api_key=API_KEY, feed_id=None, station=None)
        print('\n'.join(list(ti.get_train_identifiers_for_all_feeds())))

