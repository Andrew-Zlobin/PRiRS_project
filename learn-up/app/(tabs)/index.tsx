import {Button, View, TouchableOpacity, Alert, Text, Image, StyleSheet, Platform } from 'react-native';

import { HelloWave } from '@/components/HelloWave';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { useColorScheme } from '@/hooks/useColorScheme';

import { useRootNavigationState, router, Redirect } from 'expo-router';


import {SafeAreaView, SafeAreaProvider} from 'react-native-safe-area-context';

// import LiveAudioStream from 'react-native-live-audio-stream';
// import MicStream from 'react-native-microphone-stream';

// const getUserMedia = require('get-user-media-promise');
// const MicrophoneStream = require('microphone-stream').default;
import { useAudioRecorder, RecordingOptions, AudioModule, RecordingPresets } from 'expo-audio';
import { useState, useEffect } from 'react';


export default function HomeScreen() {
  const colorScheme = useColorScheme();
  const theme = useColorScheme() ?? 'light';


  let access_token = localStorage.getItem("access_token");
  if (access_token == null){access_token = ""}
  console.log("access_token", access_token)
  

  // блять я надеюсь это никто не увидит
  let wsForAudio = new WebSocket('ws://localhost:8000/voiceStream/')

  fetch('http://localhost:8000/hello',
        {method: 'get', 
          headers: new Headers({
              'Authorization': 'Bearer ' + localStorage.getItem("access_token"), 
              'Content-Type': 'application/x-www-form-urlencoded'
          })}
      ).then(res => res.json()).then(((res) => {
        // if (res.status === 401) {
          console.log("try to connect to ", res)

          wsForAudio = new WebSocket('ws://localhost:8000/voiceStream/' + res); // , ["access_token", access_token]
        }
      ))

  
  let current_task = {
    key: "task_1",
    name: "Task 1. Very interestig question",
    text: "Read the sentence below: \n what I'm wasting my life on...",
    difficulty: 5
  }


  const audioRecorder = useAudioRecorder(RecordingPresets.HIGH_QUALITY);

  const record = async () => {
    await audioRecorder.prepareToRecordAsync();
    audioRecorder.record();
  };

  const stopRecording = async () => {
    // The recording will be available on `audioRecorder.uri`.
    console.log("uri = ", audioRecorder.uri)

    await audioRecorder.stop();
    console.log("uri = ", audioRecorder.uri)
    var data = new FormData()
    data.append('file', input.files[0])
    fetch('http://localhost:8000/hello',
      {method: 'post', 
        headers: new Headers({
            'Authorization': 'Bearer ' + localStorage.getItem("access_token"), 
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        body}
    )
  };

  useEffect(() => {
    (async () => {
      const status = await AudioModule.requestRecordingPermissionsAsync();
      if (!status.granted) {
        Alert.alert('Permission to access microphone was denied');
      }
    })();
  }, []);



  return (
    <ParallaxScrollView
      // headerBackgroundColor={{ light: '#A1CEDC', dark: '#1D3D47' }}
      headerBackgroundColor={{ light: '#D0D0D0', dark: '#353636' }}
      headerImage={
        // <ThemedText>Test</ThemedText>
        // <Text style={{fontSize: 50, color: colorScheme == 'light' ? 'black' : 'white', paddingTop: 100}}>Learn Up</Text>
        <Text style={styles.headerImage}>Learn Up</Text>

      }>
      <View style={{borderWidth: 2,
    borderRadius: 16,
    padding: "10%",
    borderColor: theme === 'light' ? "black" : "white"}}>
      <ThemedView style={styles.titleContainer}>
        <ThemedText type="title">{current_task.name}</ThemedText>
        {/* <ThemedText type="title">{current_task.text}</ThemedText> */}

      </ThemedView>
      <ThemedView>
        <ThemedText >Difficulty : {current_task.difficulty}</ThemedText>
        <ThemedText style={{marginBottom: 15}}>{current_task.text}</ThemedText>
      </ThemedView>

      <SafeAreaProvider>
    <SafeAreaView style={styles.container}>
      <View style={{
      width:"100%", 
      borderRadius: 8, 
      overflow: 'hidden',
      maxWidth: 500,
      
    }}>
      
        <Button
          // border-radius="30"
          title="Hold to speak"
          // onPress={() => Alert.alert('Simple Button pressed')}
          onPress={() => {record(); console.log('audio with websockets')}}
          // onPress={() => {ws.send(new TextEncoder().encode("Hello")); console.log('audio with websockets')}}
        />
        <Button
          // border-radius="30"
          title="stop"
          color="red"
          // onPress={() => Alert.alert('Simple Button pressed')}
          onPress={() => {stopRecording(); console.log('stop audio')}}
          // onPress={() => {ws.send(new TextEncoder().encode("Hello")); console.log('audio with websockets')}}
        />
        {/* <Button
          title={audioRecorder.isRecording ? 'Stop Recording' : 'Start Recording'}
          onPress={audioRecorder.isRecording ? stopRecording : record}
        /> */}
      </View>
      
      {/* <TouchableOpacity onPress={() => console.log('Button 2 pressed')
        // setIsCollapsed(false)
      } >
        <Button
            title="Press me 2"
            color='#000000'
            />
      </TouchableOpacity> */}
    </SafeAreaView>
    
  </SafeAreaProvider>
  </View>

    </ParallaxScrollView>
  );
}

// const styles = StyleSheet.create({
//   headerImage: {
//     color: '#808000',
//     bottom: 10,//-90,
//     left: 0,
//     position: 'absolute',
//     fontSize: 50
//   },
//   titleContainer: {
//     flexDirection: 'row',
//     alignItems: 'center',
//     gap: 8,
//   },
//   stepContainer: {
//     gap: 8,
//     marginBottom: 8,
//   },
//   reactLogo: {
//     height: 178,
//     width: 290,
//     bottom: 0,
//     left: 0,
//     position: 'absolute',
//   },
// });
const styles = StyleSheet.create({
  headerImage: {
    color: '#808080',
    bottom: 10,//-90,
    left: 10,
    position: 'absolute',
    fontSize: 70
  },
  titleContainer: {
    flexDirection: 'row',
    gap: 8,
    marginBottom: 15,
  },

  container: {
    flex: 1,
    justifyContent: 'center',
    // marginHorizontal: 16,
    alignItems: 'center'
  },
  title: {
    textAlign: 'center',
    marginVertical: 8,
  },
});
