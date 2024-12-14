import pymysql
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List


class ActionFetchInformation(Action):
    def name(self) -> Text:
        return "action_fetch_information"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain) -> List[Dict[Text, Any]]:
        try:
            # Lấy thông tin từ slot
            query = tracker.get_slot("subtopic")
            print(f"DEBUG: Slot value retrieved: {query}")  # Log giá trị slot
            if not query:
                dispatcher.utter_message("Please specify a valid topic or subtopic you want to know about.")
                return []

            # Truy vấn cơ sở dữ liệu
            results = self.fetch_from_database(query)
            print(f"DEBUG: Fetch results: {results}")  # Log kết quả truy vấn
            if results:
                response = self.format_response(results)
                dispatcher.utter_message(response)
            else:
                dispatcher.utter_message(f"Sorry, I couldn't find any information about '{query}'.")

        except Exception as e:
            dispatcher.utter_message(f"An unexpected error occurred: {str(e)}")
            print(f"ERROR: {e}")  # Log lỗi chi tiết

        return []

    def fetch_from_database(self, query: str) -> List[Dict[Text, Any]]:
        """
        Truy vấn thông tin từ cơ sở dữ liệu MySQL.
        """
        connection = None
        try:
            print("DEBUG: Connecting to database...")  # Log kết nối
            connection = pymysql.connect(
                host="localhost",
                user="root",
                password="1234",
                database="rasa",
                cursorclass=pymysql.cursors.DictCursor
            )
            print("DEBUG: Database connected.")  # Log kết nối thành công

            with connection.cursor() as cursor:
                sql = """
                    SELECT 
                        c.name AS chapter_name, 
                        t.name AS topic_name, 
                        s.name AS subtopic_name,
                        d.description AS detail_description, 
                        d.conditions, 
                        d.characteristics,
                        e.example_description, 
                        e.application
                    FROM chapter c
                    LEFT JOIN topics t ON c.chapter_id = t.chapter_id
                    LEFT JOIN subtopics s ON t.topic_id = s.topic_id
                    LEFT JOIN details d ON s.subtopic_id = d.subtopic_id
                    LEFT JOIN examples e ON d.detail_id = e.detail_id
                    WHERE c.name LIKE %s OR t.name LIKE %s OR s.name LIKE %s
                """
                print(f"DEBUG: Executing SQL query: {sql}")  # Log SQL query
                cursor.execute(sql, ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
                results = cursor.fetchall()
                print(f"DEBUG: Query results: {results}")  # Log kết quả
                return results
        except pymysql.MySQLError as e:
            print(f"MySQL Error: {e}")  # Log lỗi MySQL
            raise RuntimeError(f"Database query failed: {e}")
        finally:
            if connection:
                connection.close()
                print("DEBUG: Database connection closed.")  # Log đóng kết nối

    def format_response(self, results: List[Dict[Text, Any]]) -> str:
        """
        Format lại phản hồi dựa trên kết quả truy vấn.
        """
        response = ""
        for row in results:
            response += (
                f"**Chapter:** {row.get('chapter_name', 'N/A')}\n"
                f"**Topic:** {row.get('topic_name', 'N/A')}\n"
                f"**Subtopic:** {row.get('subtopic_name', 'N/A')}\n"
                f"**Details:** {row.get('detail_description', 'N/A')}\n"
                f"**Conditions:** {row.get('conditions', 'N/A')}\n"
                f"**Characteristics:** {row.get('characteristics', 'N/A')}\n"
                f"**Example:** {row.get('example_description', 'N/A')} "
                f"(Application: {row.get('application', 'N/A')})\n\n"
            )
        print(f"DEBUG: Formatted response: {response.strip()}")  # Log phản hồi
        return response.strip()
