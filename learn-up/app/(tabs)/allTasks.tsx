import {Text, StyleSheet, Image, Platform } from 'react-native';

import { Collapsible } from '@/components/Collapsible';
import { ExternalLink } from '@/components/ExternalLink';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { IconSymbol } from '@/components/ui/IconSymbol';
import { useColorScheme } from '@/hooks/useColorScheme';
import { router , Redirect} from 'expo-router';
import { useState} from 'react';


export default function AllTasksScreen() {


  const colorScheme = useColorScheme();
  let styleForParallax = styles.headerImage
  styleForParallax.color = colorScheme == 'light' ? 'black' : 'white'

  let tasks = [{
    "key": "Placeholder",
    "name": "Placeholder",
    "text": "text placeholder",
    "difficulty": -1},];


    let [tasksList, setTasksList] = useState(tasks.map((task : any)  => 
      <Collapsible key={task.key} title={task.name}>
        <ThemedText>
          Task difficulty : {task.difficulty}
        </ThemedText>
        <ThemedText type="defaultSemiBold">{task.text}</ThemedText>
  
      </Collapsible>
    ))


  // fetch('http://localhost:8000/allTasks',
  //       {method: 'get', 
  //         headers: new Headers({
  //             'Authorization': 'Bearer ' + localStorage.getItem("access_token"), 
  //             'Content-Type': 'application/x-www-form-urlencoded'
  //         })}
  //     ).then(res => res.json()).then(((res) => {
        
  //         // console.log("tasks response", new TextDecoder().decode(res.body))
  //         // console.log("Pizdec bl'at'", res)
  //         // setTasks({ value: res, error: '' })
  //         tasks = res
  //         setTasksList(tasks.map((task : any)  => 
  //           <Collapsible key={task.key} title={task.name}>
  //             <ThemedText>
  //               Task difficulty : {task.difficulty}
  //             </ThemedText>
  //             <ThemedText type="defaultSemiBold">{task.text}</ThemedText>
      
  //           </Collapsible>
  //         ))
        
  
  //     }))

  

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#D0D0D0', dark: '#353636' }}
      headerImage={
        <Text style={styleForParallax}>Past and upcoming</Text>
      }>
      
      {tasksList}


    </ParallaxScrollView>
  );
}

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
  },
});
