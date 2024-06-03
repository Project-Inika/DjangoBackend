import requests

def extract_substring(s):
    """
    Extracts a valid substring without extra special characters.
    
    :param s: String
    :returns: Valid substring without extra special characters.
    """
    start_index = s.find("[")
    end_index = s.find("]")

    if start_index != -1 and end_index != -1 and end_index > start_index:
        return s[start_index + 1:end_index].strip()
    else:
        return ""  # or handle invalid cases

def process_paths(urls_array, prefix, uid):
    processed_paths = []
    
    for path in urls_array:
        index = path.find(uid)
        if index != -1:
            substring_index = index + len(uid)
            processed_paths.append(prefix + path[substring_index:])
        else:
            print(path)
            processed_paths.append(path)
    
    return processed_paths

def remove_last_characters(strings, num):
    """
    Remove the last #count number of characters from each string in the list.

    :param strings: List of strings
    :param count: Number of characters to remove from the end of each string
    :returns: List of strings with the last #count characters removed
    """
    return [s[:-num] for s in strings]

def process_text(text, uid):
    """
    Wrapper method for API call to server for semantic search.

    :param text: String
    :param uid: String
    :returns: JSON response data from the API call
    """
    print("1")
    try:
        response_class = requests.post("https://cheaply-shining-pup.ngrok-free.app/cbot", json={
            'uid': uid,
            'message': text
        })
        response_query_store = requests.post(
            "https://us-central1-inika-webpage.cloudfunctions.net/StoreQuery",
            json={'query': text, 'query_type': 'Semantic'}
        )

        # Ensure both requests were successful
        response_class.raise_for_status()
        response_query_store.raise_for_status()

        print("Success 1")
        return response_class.json()
    except requests.RequestException as e:
        print(f"Error during API call: {e}")
        return None

def process_text2(text, uid):
    """
    Wrapper method for API call to server for general search.

    :param text: String
    :param uid: String
    :returns: JSON response data from the API call
    """
    print("2")
    try:
        response_class = requests.post("https://cheaply-shining-pup.ngrok-free.app/searchQuery", json={
            'uid': uid,
            'message': text
        })
        response_query_store = requests.post(
            "https://us-central1-inika-webpage.cloudfunctions.net/StoreQuery",
            json={'query': text, 'query_type': 'General'}
        )

        # Ensure both requests were successful
        response_class.raise_for_status()
        response_query_store.raise_for_status()

        return response_class.json()
    except requests.RequestException as e:
        print(f"Error during API call: {e}")
        return None

def process_image(imagedata):
    """
    Makes call to server for image categorization and general search.

    :param imagedata: The image data to be processed
    :returns: The response data from the second API call
    """
    try:
        # First API call to categorize the image
        response = requests.post(
            "https://us-central1-inika-webpage.cloudfunctions.net/imageCategory",
            json={'image': imagedata}
        )
        response.raise_for_status()
        index = response.json().get('imageIndex')
        print(index)

        # Second API call to search with the image and category index
        response2 = requests.post(
            "https://sunfish-pure-internally.ngrok-free.app/search",
            json={'image': imagedata, 'cat': index}
        )
        response2.raise_for_status()
        return response2.json()
    
    except requests.RequestException as error:
        print(f"Error uploading file: {error}")
        return None