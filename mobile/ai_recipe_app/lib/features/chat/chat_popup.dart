import 'package:flutter/material.dart';
import '../../core/api_client.dart';


class ChatPopup extends StatefulWidget {
  final VoidCallback onClose;

  const ChatPopup({super.key, required this.onClose});

  @override
  State<ChatPopup> createState() => _ChatPopupState();
}

class _ChatPopupState extends State<ChatPopup> {
  final TextEditingController _controller = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Positioned(
      bottom: 20,
      right: 20,
      left: 20,
      child: Material(
        elevation: 12,
        borderRadius: BorderRadius.circular(16),
        child: Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(16),
            color: Colors.white,
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [

              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    "AI Chef 🤖",
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  IconButton(
                    onPressed: widget.onClose,
                    icon: const Icon(Icons.close),
                  ),
                ],
              ),

              const SizedBox(height: 8),

              const Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  "Hey there 👋 What do you want to cook today?",
                  style: TextStyle(fontSize: 14),
                ),
              ),

              const SizedBox(height: 12),

              Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _controller,
                      decoration: const InputDecoration(
                        hintText: "Type ingredients or recipe...",
                        border: OutlineInputBorder(),
                        isDense: true,
                      ),
                    ),
                  ),

                  const SizedBox(width: 8),

                  IconButton(
                    icon: const Icon(Icons.send, color: Colors.green),
                    onPressed: () async {
                      final text = _controller.text.trim();

                      if (text.isEmpty) return;

                      print("Sending: $text");

                      try {

                      final result = await ApiClient.sendChatMessage(text);

                      print("Backend response:");
                      print(result);

                    } catch (e) {
                      print("API Error: $e");
                    }
                    _controller.clear();
                    },
                  )
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
