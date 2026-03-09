import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re


nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')


txt = """AIPAC should be registered as a foreign agent meddling in US
elections. American Israel Political Action Committee. It is
interfering in the US electoral process and should be put on trial
and it's leaders imprisoned. @benshapiro @charliekirk11
https://t.cofebO4iPUah8"""

# Step 1: Lowercase the entire text
# "Hello World" -> "hello world"
txt = txt.lower()

# Step 2: Remove URLs (anything starting with http or www)
# "visit https://example.com today" -> "visit  today"
txt = re.sub(r'http\S+|www\S+', ' ', txt)

# Step 3: Remove @mentions
# "@benshapiro said" -> " said"
txt = re.sub(r'@\S+', ' ', txt)

# Step 4: Remove anything that is NOT a letter or whitespace
# removes: . , ! ? ( ) ' " # $ % etc.
# "it's good." -> "its good"
txt = re.sub(r'[^a-z\s]', '', txt)

# Step 5: Collapse multiple spaces into one
# "hello    world" -> "hello world"
txt = re.sub(r'\s+', ' ', txt).strip()

# Get English stopwords and tokenize
stop_words = set(stopwords.words('english'))
tokens = word_tokenize(txt.lower())


# Remove stopwords
filtered_tokens = [word for word in tokens if word not in stop_words]

print("Filtered:", filtered_tokens)