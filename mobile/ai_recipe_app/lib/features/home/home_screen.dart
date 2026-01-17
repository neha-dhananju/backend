import 'dart:async';
import 'package:flutter/material.dart';
import '../chat/chat_popup.dart';
import 'category_widget.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {

  bool showChat = false;

  @override
  void initState() {
    super.initState();

    // Show chat popup after 2 seconds
    Timer(const Duration(seconds: 2), () {
      setState(() {
        showChat = true;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("AI Recipe App"),
      ),
      body: Stack(
        children: [

          // Main content
          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [

                const Text(
                  "Categories",
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),

                const SizedBox(height: 12),

                SizedBox(
                  height: 160,
                  child: ListView(
                    scrollDirection: Axis.horizontal,
                    children: [

                      CategoryWidget(
                        title: "Veg",
                        imagePath: "assets/categories/veg.png",
                        onTap: () {
                          print("Veg clicked");
                        },
                      ),

                      CategoryWidget(
                        title: "Non-Veg",
                        imagePath: "assets/categories/nonveg.png",
                        onTap: () {
                          print("Non-Veg clicked");
                        },
                      ),

                      CategoryWidget(
                        title: "Vegan",
                        imagePath: "assets/categories/vegan.png",
                        onTap: () {
                          print("Vegan clicked");
                        },
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),

          // Chat Popup Overlay
          if (showChat)
            ChatPopup(
              onClose: () {
                setState(() {
                  showChat = false;
                });
              },
            ),
        ],
      ),
    );
  }
}
