from settings import conf


VIEWS_STREAM = f"""
CREATE TABLE IF NOT EXISTS views (
    user_id Int64,
    movie_id UUID,
    movie_timestamp Int32,
    date_time DateTime
) Engine = MergeTree
PARTITION BY toYYYYMM(date_time)
ORDER BY (user_id, movie_id, date_time);

CREATE TABLE IF NOT EXISTS views_queue (
    user_id Int64,
    movie_id UUID,
    movie_timestamp Int32,
    date_time DateTime
)
ENGINE = Kafka
SETTINGS    kafka_broker_list = '{conf.KAFKA_HOST}:{conf.KAFKA_PORT}',
            kafka_topic_list = '{conf.KAFKA_TOPIC}',
            kafka_group_name = '{conf.KAFKA_GROUP}',
            kafka_format = 'JSONEachRow',
            kafka_skip_broken_messages = 5;

CREATE MATERIALIZED VIEW IF NOT EXISTS views_queue_mv TO views AS
    SELECT user_id, movie_id, movie_timestamp, date_time
    FROM views_queue;
"""
