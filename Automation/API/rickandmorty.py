import requests
import requests_cache
import json
from tqdm import tqdm
import time


class RickAndMortyAPI:
    def __init__(self):
        self.base_url = "https://rickandmortyapi.com/api"
        self.character_url = f"{self.base_url}/character"
        self.location_url = f"{self.base_url}/location"
        self.episode_url = f"{self.base_url}/episode"
        self.cache = requests_cache.CachedSession(cache_name='rick_and_morty_cache',
                                                  backend='sqlite',
                                                  expire_after=3600)

    def _make_request(self, url, params=None):
        start_time = time.time()
        try:
            response = self.cache.get(url, params=params)
            if response is None:
                response = requests.get(url, params=params)
                response.raise_for_status()
                elapsed_time = time.time() - start_time
                if elapsed_time > 0.2:
                    with tqdm(total=100, desc="Fetching data") as pbar:
                        pbar.update(50)
                        # noinspection PyUnresolvedReferences
                        self.cache.set(url, response)
                        pbar.update(50)
                else:
                    # noinspection PyUnresolvedReferences
                    self.cache.set(url, response)
            data = response.json()
            return data
        except (requests.RequestException, json.JSONDecodeError) as e:
            print(f"An error occurred while fetching data from {url}: {e}")
            return None

    def get_count(self, route):
        url = f"{self.base_url}/{route}"
        data = self._make_request(url)
        if data:
            return data.get('info', {}).get('count')
        print(f"Failed to get count for {route}.")
        return None

    def get_all_characters(self):
        all_characters = []
        page = 1
        while True:
            response = self._make_request(f"{self.character_url}?page={page}")
            if response:
                page_characters = response.get('results', [])
                all_characters.extend(page_characters)
                if response['info']['next']:
                    page += 1
                else:
                    break
        return all_characters

    def get_episodes_for_character(self, character_name):
        all_characters = self.get_all_characters()
        if all_characters:
            for character in all_characters:
                if character['name'] == character_name:
                    return character['episode']
            print(f"Character {character_name} not found.")
        return None

    def get_id_by_character_name(self, character_name):
        params = {"name": character_name}
        response = self._make_request(self.character_url, params=params)
        if response:
            results = response.get("results", [])
            if results:
                return results[0]["id"]
            else:
                print(f"Character {character_name} not found.")
        return None

    def get_status_from_character(self, character_name):
        all_characters = self.get_all_characters()
        if all_characters:
            for character in all_characters:
                if character['name'] == character_name:
                    return character['status']
            print(f"Character {character_name} not found.")
        return None

    def get_location_from_character(self, character_name):
        all_characters = self.get_all_characters()
        if all_characters:
            for character in all_characters:
                if character['name'] == character_name:
                    return character['location']['name']
            print(f"Character {character_name} not found.")
        return None

    def get_alive_characters_in_location(self, location):
        all_characters = self.get_all_characters()
        if all_characters:
            alive_characters_in_location = [character['name']
                                            for character in all_characters
                                            if character['status'] == 'Alive' and
                                            character['location']['name'] == location]
            return alive_characters_in_location
        return None

    def get_characters_from_episode(self, episode_number):
        try:
            episode_url = f"{self.episode_url}/{episode_number}"
            response = self._make_request(episode_url)
            if response:
                characters_urls = response.get('characters', [])
                character_ids = [int(url.split('/')[-1]) for url in characters_urls]
                return character_ids
        except Exception as e:
            print(f"Failed to get characters from episode {episode_number}: {e}")
        return None

    def get_character_by_id(self, character_id):
        try:
            character_url = f"{self.character_url}/{character_id}"
            return self._make_request(character_url)
        except Exception as e:
            print(f"Failed to get character with id {character_id}: {e}")
            return None

    def get_characters_with_name_contains(self, character_name_part, episode_number):
        character_ids = self.get_characters_from_episode(episode_number)
        if character_ids:
            try:
                characters_with_name_contains = [self.get_character_by_id(character_id)['name']
                                                 for character_id in character_ids
                                                 if character_id]
                return [name for name in characters_with_name_contains if character_name_part in name]
            except Exception as e:
                print(f"Failed to get characters with name containing '{character_name_part}' "
                      f"from episode {episode_number}: {e}")
        return None

    def get_non_alive_characters_from_episode(self, episode_number):
        character_ids = self.get_characters_from_episode(episode_number)
        if character_ids:
            try:
                non_alive_characters = [self.get_character_by_id(character_id)['name']
                                        for character_id in character_ids
                                        if character_id and self.get_character_by_id(character_id)['status'] != 'Alive']
                return non_alive_characters
            except Exception as e:
                print(f"Failed to get non-alive characters from episode {episode_number}: {e}")
        return None

    def get_species_and_characters_from_season(self, season_number):
        try:
            url = self.episode_url
            params = {"episode": f"S0{season_number}"}
            response_data = self._make_request(url, params=params)
            if response_data:
                species_dict = {}
                for result in response_data.get("results", []):
                    characters_urls = result.get("characters", [])
                    for url in characters_urls:
                        character_id = url.split("/")[-1]
                        all_species = self._get_species_of_character(character_id)
                        if all_species:
                            character_data = self._get_character(character_id)
                            if all_species != "Human" and character_data:
                                species_dict.setdefault(all_species, []).append(character_data["name"])
                return species_dict
        except Exception as e:
            print(f"Failed to get species and characters from season {season_number}: {e}")
            return None

    def _get_species_of_character(self, character_id):
        try:
            character_url = f"{self.base_url}/character/{character_id}"
            response_data = self._make_request(character_url)
            if response_data:
                return response_data.get("species")
        except Exception as e:
            print(f"Failed to get species of character with id {character_id}: {e}")
            return None

    def _get_character(self, character_id):
        try:
            character_url = f"{self.base_url}/character/{character_id}"
            response_data = self._make_request(character_url)
            if response_data:
                return response_data
        except Exception as e:
            print(f"Failed to get character with id {character_id}: {e}")
            return None


rick_and_morty_api = RickAndMortyAPI()


def print_exercise_header(exercise_number):
    print(f"\nExercise {exercise_number}")


def print_results(message, results):
    print(message)
    if results:
        for result in results:
            print(result)
    else:
        print("No results found.")


print_exercise_header(1)
print_results("Get the Character id of Rick Sanchez",
              [rick_and_morty_api.get_id_by_character_name("Rick Sanchez")])

print_exercise_header(2)
rick_status = rick_and_morty_api.get_status_from_character("Rick Sanchez")
morty_status = rick_and_morty_api.get_status_from_character("Morty Smith")
rick_location = rick_and_morty_api.get_location_from_character("Rick Sanchez")
morty_location = rick_and_morty_api.get_location_from_character("Morty Smith")
print(f"Rick Sanchez is currently {rick_status} and located in {rick_location}.")
print(f"Morty Smith is currently {morty_status} and located in {morty_location}.")

print_exercise_header(3)
print_results("Get all the episodes where 'Gene' has appeared, and the location for him.",
              [rick_and_morty_api.get_episodes_for_character("Gene")])

print_exercise_header(4)
alive_characters_in_narnia = rick_and_morty_api.get_alive_characters_in_location("Narnia Dimension")
print_results("List all the characters who are alive and appeared in the 'Narnia Dimension', "
              "regardless of episode or season", alive_characters_in_narnia)

print_exercise_header(5)
rick_characters_in_episode_28 = rick_and_morty_api.get_characters_with_name_contains("Rick",
                                                                                     28)
print_results("From episode 28, list all the characters who have 'Rick' in their name.",
              rick_characters_in_episode_28)

print_exercise_header(6)
non_alive_characters_in_episode_29 = rick_and_morty_api.get_non_alive_characters_from_episode(29)
print_results("List all the characters who are not Alive from episode 29.",
              non_alive_characters_in_episode_29)

print_exercise_header(7)
species_and_characters = rick_and_morty_api.get_species_and_characters_from_season(3)
if species_and_characters:
    for species, characters in species_and_characters.items():
        print(f"Species: {species}")
        print(f"Characters: {', '.join(characters)}")
        print()
else:
    print("Failed to fetch data for Season 3.")
