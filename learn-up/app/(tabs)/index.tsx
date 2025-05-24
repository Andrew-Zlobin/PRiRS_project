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
import { ColorSpace } from 'react-native-reanimated';


export default function HomeScreen() {
  const colorScheme = useColorScheme();
  const theme = useColorScheme() ?? 'light';


  let access_token = localStorage.getItem("access_token");
  if (access_token == null){access_token = ""}
  console.log("access_token", access_token)
  
  let [record_button_switcher, set_record_button_switcher]= useState(false);
  // блять я надеюсь это никто не увидит
  // let wsForAudio = new WebSocket('ws://localhost:8000/voiceStream/')

  fetch('http://localhost:8000/hello',
        {method: 'get', 
          headers: new Headers({
              'Authorization': 'Bearer ' + localStorage.getItem("access_token"), 
              'Content-Type': 'application/x-www-form-urlencoded'
          })}
      ).then(res => res.json()).then(((res) => {
        // if (res.status === 401) {
          console.log("try to connect to ", res)

          // wsForAudio = new WebSocket('ws://localhost:8000/voiceStream/' + res); // , ["access_token", access_token]
        }
      ))

  
  let [current_task, set_current_task] = useState({
    key: "task_placeholder",
    name: "Task 1. Task placeholder name",
    text: "Read the sentence below: \n what I'm wasting my life on...",
    difficulty: 5
  })

  let [colorised_text_view, set_colorised_text_view] = useState();
  let [list_of_errors, set_list_of_errors] = useState([]);
  let [is_done, set_is_done] = useState(false);

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
        const response = await fetch("http://localhost:8000/currentTask",
          {
            method: 'get', 
            headers: new Headers({
                'Authorization': 'Bearer ' + localStorage.getItem("access_token"), 
                'Content-Type': 'application/x-www-form-urlencoded'
            })});
        // console.log("response ^ ", response);
        if (response.ok) {
          const result = await response.json();
          set_current_task(result);
        }
        
        // console.log(result.status)
        // 
    } catch (error) {
        console.error("Error fetching data:", error);
    } finally {
        setLoading(false);
    }
};
  useEffect(() => {
    fetchData();
}, []);

  const audioRecorder = useAudioRecorder(RecordingPresets.HIGH_QUALITY);
  
  async function sendFileFromBlob(blobUri : string, uploadUrl:string) {
    try {
        // Fetch the blob data from the URI
        const response = await fetch(blobUri);
        const blob = await response.blob();
        console.log(blob)
        // Create a File from the Blob (if needed, adjust the filename and MIME type)
        const file = new File([blob], "sentence.webm", { type: blob.type });

        // Create FormData and append the file
        const formData = new FormData();
        formData.append("file", file);

        // Send the file via POST request
        const uploadResponse = await fetch(uploadUrl, {
            method: "POST",
            body: formData,
            headers: new Headers({
              'Authorization': 'Bearer ' + localStorage.getItem("access_token"),
          })
        });

        // Handle the response
        const result = await uploadResponse.json();
        console.log("failed", result)
        console.log("Upload success:", result);
        set_list_of_errors(result.res);
        set_is_done(true);
        console.log(list_of_errors);
    } catch (error) {
        console.error("Error uploading file:", error);
    }
  }
  const record = async () => {
    await audioRecorder.prepareToRecordAsync();
    audioRecorder.record();
  };

  const stopRecording = async () => {
    // The recording will be available on `audioRecorder.uri`.
    console.log("uri = ", audioRecorder.uri);

    await audioRecorder.stop();
    console.log("uri = ", audioRecorder.uri);
    
    sendFileFromBlob( audioRecorder.uri  !== null ? audioRecorder.uri : "", "http://localhost:8000/getAudio");
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
        {/* <ThemedText >Difficulty : {current_task.difficulty}</ThemedText> */}
        <ThemedText style={{marginBottom: 30}}>{current_task.text.split(" ").map((word : any, index)  => 
                                // <ThemedText key={index}>{word} </ThemedText>
                                <Text key={index} style={{color: list_of_errors.includes(index) ? "red" : "black"}}>{word} </Text>
                              )}</ThemedText>
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
          title={record_button_switcher ? "Stop recording" : "Press and speak"}
          onPress={() => {if (record_button_switcher)
                           {set_record_button_switcher(false); stopRecording(); console.log('stop audio')}
                          else
                           {set_record_button_switcher(true); record(); console.log('audio with websockets');}}}
        />
        
      </View>
      {is_done ? <View style={{
        width:"100%",
        marginTop: 20, 
        borderRadius: 8, 
        overflow: 'hidden',
        maxWidth: 500,
      }}>
        <Button
            title="Next task"
            onPress={() => {fetchData(); set_list_of_errors([]); set_is_done(false);}}
          />
        </View>: ""}
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
