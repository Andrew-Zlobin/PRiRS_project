import {Text, StyleSheet, Image, Platform } from 'react-native';

import { Collapsible } from '@/components/Collapsible';
import { ExternalLink } from '@/components/ExternalLink';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { IconSymbol } from '@/components/ui/IconSymbol';
import { useColorScheme } from '@/hooks/useColorScheme';
import { router , Redirect} from 'expo-router';
import { useEffect, useState} from 'react';


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

    const [loadingTasks, setLoadingTasks] = useState(false);
    
      const fetchData = async () => {
        setLoadingTasks(true);
        try {
            const response = await fetch("http://localhost:8000/allTasks",
              {
                method: 'get', 
                headers: new Headers({
                    'Authorization': 'Bearer ' + localStorage.getItem("access_token"), 
                    'Content-Type': 'application/x-www-form-urlencoded'
                })});
    
            const result = await response.json();
            tasks = result
            console.log(result)
            setTasksList(tasks.map((task : any)  => 
                        <Collapsible key={task.key} title={task.name}>
                          <ThemedText>
                            Task difficulty : {task.difficulty}
                          </ThemedText>
                          <ThemedText type="defaultSemiBold">{task.text}</ThemedText>
                  
                        </Collapsible>
                      ))

          } catch (error) {
            console.error("Error fetching data:", error);
        } finally {
          setLoadingTasks(false);
        }
    };
      useEffect(() => {
        fetchData();
    }, []);

  

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
