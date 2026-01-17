import 'package:flutter/material.dart';
import 'core/theme.dart';
import 'features/home/home_screen.dart';

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'AI Recipe App',
      theme: AppTheme.lightTheme,
      home: const HomeScreen(),
    );
  }
}
