import { Tabs } from 'expo-router';
import React from 'react';
import { Dimensions, Platform } from 'react-native';

import { HapticTab } from '@/components/HapticTab';
import { IconSymbol } from '@/components/ui/IconSymbol';
import TabBarBackground from '@/components/ui/TabBarBackground';
import { Colors } from '@/constants/Colors';
import { useColorScheme } from '@/hooks/useColorScheme';

import Ionicons from '@expo/vector-icons/Ionicons';
import { useRootNavigationState, router, Redirect } from 'expo-router';



export default function TabLayout() {
  const colorScheme = useColorScheme();
  const { width, height } = Dimensions.get('window');
  const isLargeScreen = width > 600

  function checkLogin(e: any) {
    // Prevent default action
    // if (rootNavigationState?.key) {
    console.log("token : ", localStorage.getItem("access_token"))
    fetch('http://localhost:8000/hello',
      {method: 'get', 
        headers: new Headers({
            'Authorization': 'Bearer ' + localStorage.getItem("access_token"), 
            'Content-Type': 'application/x-www-form-urlencoded'
        })}
    ).then(((res) => {
      if (res.status === 401) {
        console.log("try to redirect to login")
        // return <Redirect href="/LoginScreen" />;
        router.navigate('/(tabs)/LoginScreen')
      }
      else {
        console.log("allready logined", res)
        e.preventDefault();
      }

    }))

    

    //Any custom code here
    // alert(123);
  }



  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: Colors[colorScheme ?? 'light'].tint,
        headerShown: false,
        tabBarButton: HapticTab,
        tabBarBackground: TabBarBackground,
        tabBarPosition: isLargeScreen ? 'left' : 'bottom',
        tabBarShowLabel: isLargeScreen,

        animation: 'shift',
        
        // TransitionSpecs: TransitionSpecs.FadeSpec,
        tabBarStyle: Platform.select({
          ios: {
            // Use a transparent background on iOS to show the blur effect
            position: 'absolute',
          },
          default: {},
        }),
      }}>
      <Tabs.Screen
        name="allTasks"
        options={{
          title: 'Tasks',
          // tabBarIcon: ({ color }) => <IconSymbol size={28} name="house.fill" color={color} />,
          tabBarIcon: ({ color }) => <Ionicons name="list-outline" size={28} color={color} />,
        }}
        listeners={{tabPress: checkLogin}}

      />
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          tabBarIcon: ({ color }) => <Ionicons name="home-outline" size={28} color={color} />,
        }}
        listeners={{tabPress: checkLogin}}
      />
      <Tabs.Screen
        name="settings"
        options={{
          title: 'Settings',
          tabBarIcon: ({ color }) => <Ionicons name="person-circle-outline" size={28} color={color} />,
        }}
        listeners={{tabPress: checkLogin}}

      />

      <Tabs.Screen
        name="LoginScreen"
        options={{
          href: null
          // title: 'Settings',
          // tabBarIcon: ({ color }) => <Ionicons name="person-circle-outline" size={28} color={color} />,
        }}
      />
    </Tabs>
  );
}
