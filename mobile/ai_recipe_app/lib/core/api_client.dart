import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiClient {

  // CHANGE THIS TO YOUR RENDER URL
  static const String baseUrl =
      "https://ai-recipe-app-mjok.onrender.com";

  static Future<Map<String, dynamic>> sendChatMessage(String message) async {

    final url = Uri.parse("$baseUrl/api/chat");

    final response = await http.post(
      url,
      headers: {
        "Content-Type": "application/json",
      },
      body: jsonEncode({
        "message": message,
      }),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Chat API failed");
    }
  }
}
