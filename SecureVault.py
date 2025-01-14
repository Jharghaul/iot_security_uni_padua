import hmac
import hashlib

masterkeys = ["doagW31MNuBTnvbrlDikILQI08vEBhZyhIRI96pc4RcmEimFOjtfbvqrNQ1COlBmclqrUS9T62LhH26W7SCGoAjRfNUfNBjUqudXRpZkIuBdJWwRUVT1cJ419mhvTJqj1IilXxOpoyq3gfIlEqz6liZCgKeWujdlis316syZPIOfOHnBf7fKQhFWQabmpX4JjhUscifhFg12AxrtKE0ncqjZTpq3oPMCzpFrvQIcCjcinedRuoZdHTbTYiLlpGwBvYwi5zVTyBxbkABFT5JnRMJQ6EIlEYHAHn6bQ7HMjzCuX1sgleR63cieaqD5kTwOw5KmyfUj8U4BVRCqaCpdqP2eYMZZ6Pp2yv5F88CixRfldhQiWY9rywXegMenVit5653EU4shrYxplTomfZrqqkz5AAktUEFmEPq6t17hxOlpPIEKDm53VDWIXwMvXzoBEfuo5xwxiOJroymg2vekoVbRikKZm7uqX6fA8voyOcs67LVci3c5LNbb15XT8zBJ",
              "9h6OkimozvXV0oq34IBxzer7PFKklUegEj5veAoAT1gfphfzDIABEZdZVWpV4X8qRZruHubdfWV4TRbgsSQoDOlAjlYfHfWBK7MHt7P9YitA7yuAgb1veFYVpU5ChTlpLNqTCnGYeugGJVJoLgrZpqy0eEctMQKqCwBs52p8dCMnRhBDEXPp4iOKJ4Nk4JYU6L3JgzOvmIDvhtgnMEIlc30q5w3qg5UBgTnjktvKrrIZxpn0N1UUEuOH8l91oBTUXoqLotuDEItJCH0Y5aWg8BUd8ZEtbRMbJkdvXVwTGb47DGhE3xE26s8Ipo32T9PboKQOnQCudA59ZLL8uPB9wqCbJsTQ6fJQ8udZ7q6l6EldNOyW2rjNFJCGBB7S8YkLZPbq5GUUeatSov2PpfcqBfW7ANxPvsJA0fB1Rs6kGAUpwK7KGqvU5Z2HqCld3hsQf83wbUb5BiPkoK6ajV5IUNG0AZ0tPEiC1ClsUe1TZyEGLDcKwbziat8jZkhyAbqv",
              "NULnw18OjRw8c0d397CpqAGqF3JZunBsxqY6rkOlbKxrQpJuDgeKRVv4xaVJvxrC2stMqVaz1TDo0bQcvZIHilkNgYeODYa1dnVdCpVU1ew76t8AuKJh8SN7SAoKD1u6NshQohLu1LswAoEaTAgnJbm6PhB0cTIRwxjh87DLEPib0pzSM5H0cI8ds0gmxK8BQNSra5IX6Z56sC2Nk1T53gKmLN7InQNtROibqEvCCTTwjPSGadw3c2VQbe7WrCkbH1Xm13CzhsOJWqAfBAxXE5H2KTfYprAdIYABxZZyvPnrVwyk5kqzu1njseMyErr9nRRk0h2Lso8UpR9xhEuOXJISoeSPZFrQ4tKdCBxja1DCWtY5oSSjfRSnZ3Q4IaAfI464sNYy2Jt2vZamzPcDqvnKqNYKYxk4crzcp9hggTyCnXJDOAcDAEHtSwdrI74v1aTbAzA1vRZeogyp00cC85i3FIP4j3V6pXudQ3JKHleQ9kYRZ2XaxDjWT9kRvOX",
              "Kc4OWE4xcPrHm2fWn0T6au4EHYGq7CwutuzYTfihew13DS6IuB7irBA7uyWjPQVtOaYbSHr7YOJ6v2pq3ICMOF3WVJXR5fNC6htJPgpvB7KsTQA0ZRZqq9OZRMCDOsbW8Mu9tErjrmEHxGDsakjI8xV1Ww2lAjjuuZPFypjKwSz3UjSdTCGkGY3sAMzLsYYs7kjb9vtyDM6Z7L9lWaTKhfO3WXsEYMUldFrNYEOdtrDg7u95w1FxGW1YWdATq7aH8KrQp4eXNGAEx1KWCcYR9nIqZOZlGoNO8jC0qMuvUA4cPUnzom01U7X3gnTeo13KKs1gArkxmGjiilJsdAwflF2W3R97GvNIqhb8HvKzQ7PrVA95sO1iUTBBoiR5C71FoZPbBkgX6zALDRpUyY12271Nqh7eTuFyTk4XnYg8RKzCv5ShUPwWmH87Q9voHviNzWKOOpoos8xjV8B6Bygd70DF2nhdscRM8bnnRVUdcpkvxl4oh4IeKe1UYnDGMUIa",
              "kDJzv7kw12nNnc0AgQ5sYg2tKoevjX8wC0d64Dtmk8bRsDMExHNsEbfn8RabictgsLyt5ZbU0h38tGgXjKuxyIjwGYWjIOspZNLjPYMHAtNGyqeGKI9NrlV43G9tSjwVhPekpi4FAiYBzXJxTMd1GGtgIOQccwOX8w6MmJ6OJ0uJMcGbgb4pV3wMVElleYVd1L2p5YYRdhibWo0udRlQJ0gnmDqjULMbJClGn508sixnsuCOZocppDBzMlWVUGkgdjVniCa6FfZcKjxxVxh6kt40L1vECmXglp2YkX1BzEFE6Xm0qhtV2Q2W64ZIgFuSe1PJSrhiQaohXQZ1VO3NQkiiJHw6KswObKBIh9zuBhNNtTJvE3AeLI0nnIaGp9VJjw1c9Egua489Bw0vOD5D22XleNe18uRZI75PyiZsOe3Jv8IiGiJkGdK6utLHfIrULOZPg5mjlK1UIimqajnZ7cZmXg3H7DdH08vzdhPB26D4751sE3dk0T9NvEsiYj9g"]

keys = []
digestMode = hashlib.sha256
key_length_bits = digestMode().digest_size * 8

#TODO: description
def initialize(number, digestmode=hashlib.sha256):
    
    digestMode = digestmode

    for i in range(number):
        if i < 5:
            hmacObj = hmac.new(masterkeys[i].encode("utf-8"), None, digestMode)
            keys.append(hmacObj.digest())
        else:
            hmacObj = hmac.new(masterkeys[i%5].encode("utf-8"), keys[i-5], digestMode)
            keys.append(hmacObj.digest())
    
    if len(keys) == number:
        return True    

    return False

#TODO: description
def getKey(index):
    if index >= 0 & index < len(keys):
        return keys[index]
    
    return None

#TODO: description
def changeKeys(message):
    digest = hmac.new(keys, message.encode("utf-8"), digestMode).digest()
    
    for i in range(len(keys)):
        keys[i] = keys[i]^digest
        
        