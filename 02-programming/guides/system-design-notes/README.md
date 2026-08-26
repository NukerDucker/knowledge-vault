
# [System Design Interview - An Insider's Guide (Vol 1 and 2)](https://bytebytego.com/courses/system-design-interview)
These notes are based on the System Design Interview books - [Vol 1 and Vol 2 2nd Ed](https://www.goodreads.com/book/show/54109255-system-design-interview-an-insider-s-guide) 

Check the notes here: https://pagefy.io/system-design/system-design-interview-by-alex-xu

**Note:** These notes are a work in progress. 


 * [Chapter 1 - Scale From Zero To Millions Of Users](./01-scaling/README.md)
 * [Chapter 2 - Back-of-the-envelope Estimation](./02-back-of-the-envelope-estimation/README.md)
 * [Chapter 3 - A Framework For System Design Interviews](./03-system-design-framework/README.md)
 * [Chapter 4 - Design A Rate Limiter](./04-rate-limiter/README.md)
 * [Chapter 5 - Design Consistent Hashing](./05-consistent-hashing/README.md)
 * [Chapter 6 - Design A Key-Value Store](./06-key-value-store/README.md)
 * [Chapter 7 - Design A Unique ID Generator In Distributed Systems](./07-unique-id-generator/README.md)
 * [Chapter 8 - Design A URL Shortener](./08-url-shortener/README.md)
 * [Chapter 9 - Design A Web Crawler](./09-web-crawler/README.md)
 * [Chapter 10 - Design A Notification System](./10-notification-system/README.md)
 * [Chapter 11 - Design A News Feed System](./11-news-feed-system/README.md)
 * [Chapter 12 - Design A Chat System](./12-chat-system/README.md)
 * [Chapter 13 - Design A Search Autocomplete System](./13-search-autocomplete/README.md)
 * [Chapter 14 - Design YouTube](./14-youtube/README.md)
 * [Chapter 15 - Design Google Drive](./15-google-drive/README.md)
 * [Chapter 16 - Proximity Service](./16-proximity-service/README.md)
 * [Chapter 17 - Nearby Friends](./17-nearby-friends/README.md)
 * [Chapter 18 - Design Google Maps](./18-google-maps/README.md)
 * [Chapter 19 - Distributed Message Queue](./19-distributed-message-queue/README.md)
 * [Chapter 20 - Metrics Monitoring and Alerting System](./20-metrics-monitoring-and-alerting-system/README.md)
 * [Chapter 21 - Ad Click Event Aggregation](./21-ad-click-event-aggregation/README.md)
 * [Chapter 22 - Hotel Reservation System](./22-hotel-reservation-system/README.md)
 * [Chapter 23 - Distributed Email Service](./23-distributed-email-service/README.md)
 * [Chapter 24 - S3-like Object Storage](./24-s3-like-object-storage/README.md)
 * [Chapter 25 - Real-time Gaming Leaderboard](./25-real-time-gaming-leaderboard/README.md)
 * [Chapter 26 - Payment System](./26-payment-system/README.md)
 * [Chapter 27 - Digital Wallet](./27-digital-wallet/README.md)
 * [Chapter 28 - Stock Exchange](./28-stock-exchange/README.md)


# Additonal Resources

### Rate Limiting
- [Circuit Breaker Algorithm](https://martinfowler.com/bliki/CircuitBreaker.html)
- [Uber Rate Limiter](https://github.com/uber-go/ratelimit/blob/master/ratelimit.go)


### Consistent Hashing
- [Consistent Hashing](https://tom-e-white.com/2007/11/consistent-hashing.html)
- [CS168: Introduction and Consistent Hashing:]( http://theory.stanford.edu/~tim/s16/l/l1.pdf)
- [Apache Cassandra](http://www.cs.cornell.edu/Projects/ladis2009/papers/Lakshman-ladis2009.PDF)
- [Scaling Discord](https://blog.discord.com/scaling-elixir-f9b8e1e7c29b)
- [Google Maglev](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/44824.pdf)


### Key-Value Store
- [Amazon Dynamo](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)
- [Cassandra Architecture](https://docs.datastax.com/en/archived/cassandra/3.0/cassandra/architecture/archIntro.html)
- [Google BigTable Architecture](https://static.googleusercontent.com/media/research.google.com/en//archive/bigtable-osdi06.pdf)
- [Amazon Dynamo DB Internals](https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html)
- [Design Patterns in Amazon Dynamo DB](https://www.youtube.com/watch?v=HaEPXoXVf2k)
- [Internals of Amazon Dynamo DB](https://www.youtube.com/watch?v=yvBR71D0nAQ)


### Unique-ID Generator
- [Ticket Servers: Distributed Unique Primary Keys on the Cheap](https://code.flickr.net/2010/02/08/ticket-servers-distributed-unique-primary-keys-on-the-cheap)
- [Snowflake](https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake.html)


### Web Crawler
- [Web Crawling](http://infolab.stanford.edu/~olston/publications/crawling_survey.pdf)
- [Google Dynamic Rendering](https://developers.google.com/search/docs/guides/dynamic-rendering)



### Chat Systems
- [How Discord stores billions of messages](https://discord.com/blog/how-discord-stores-billions-of-messages)
- [Flannel: An Application-Level Edge Cache to Make Slack Scale](https://slack.engineering/flannel-an-application-level-edge-cache-to-make-slack-scale/)


### Search Autocomplete
- [How We Built Prefixy](https://medium.com/@prefixyteam/how-we-built-prefixy-a-scalable-prefix-search-service-for-powering-autocomplete-c20f98e2eff1)
- [Prefix Hash Tree](https://people.eecs.berkeley.edu/~sylvia/papers/pht.pdf)


### Youtube
- [YouTube Architecture](http://highscalability.com/youtube-architecture)
- [YouTube scalability 2012](https://www.youtube.com/watch?v=w5WVu624fY8)
- [Transcoding Videos at Scale](https://www.egnyte.com/blog/2018/12/transcoding-how-we-serve-videos-at-scale/)
- [Facebook Video Broadcasting](https://engineering.fb.com/ios/under-the-hood-broadcasting-live-video-to-millions/)
- [Netflix Video Encoding at Scale](https://netflixtechblog.com/high-quality-video-encoding-at-scale-d159db052746)
- [Netflix Shot based encoding](https://netflixtechblog.com/optimized-shot-based-encodes-now-streaming-4b9464204830)


### Google Drive
- [Differential Synchronization](https://neil.fraser.name/writing/sync/)
- [Differential Synchronization Video](https://www.youtube.com/watch?v=S2Hp_1jqpY8)
- [How We’ve Scaled Dropbox](https://www.youtube.com/watch?v=PE4gwstWhmc&feature=youtu.be)
