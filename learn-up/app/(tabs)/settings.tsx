import { StyleSheet, Button, Text, Image, Platform } from 'react-native';

import { Collapsible } from '@/components/Collapsible';
import { ExternalLink } from '@/components/ExternalLink';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import Ionicons from '@expo/vector-icons/Ionicons';

import { useColorScheme } from '@/hooks/useColorScheme';
import { router , Redirect} from 'expo-router';


export default function SettingsScreen() {

  const _onLogoutPressed = () => {
    
      // router.navigate('/(tabs)');
      console.log("try to logout")
      fetch('http://127.0.0.1:8000/logout', {
        method: 'POST',
        mode: "cors",
      }).then((res) => {
        console.log('auth res:', res);
        // if (res.ok) {
          res.json().then((data) => {
            console.log("next step must be redirection to login", data);
            localStorage.setItem("access_token", data["access_token"])
            router.navigate('/(tabs)/LoginScreen');
            // router.replace('/');
            // navigation &&
            //   navigation.navigate('Dashboard', { token: data.access_token });
          });
        // }
      });
    };


  const colorScheme = useColorScheme();
  let styleForParallax = styles.headerImage
  styleForParallax.color = colorScheme == 'light' ? 'black' : 'white'


  


  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#D0D0D0', dark: '#353636' }}
      headerImage={
        // <IconSymbol
        //   size={310}
        //   color="#808080"
        //   name="chevron.left.forwardslash.chevron.right"
        //   style={styles.headerImage}
        // />
        <Text style={styleForParallax}>Hello, User</Text>
        // <Text style={{fontSize: 50, color: colorScheme == 'light' ? 'black' : 'white', paddingTop: 100}}>Learn Up</Text>


      }>
      
      <ThemedText>Here would be settings</ThemedText>

      <Button
        title="Logout"
        color={"red"}
        onPress={_onLogoutPressed}
      />
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
