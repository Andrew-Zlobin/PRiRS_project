import { DarkTheme, DefaultTheme, ThemeProvider } from '@react-navigation/native';
import { useFonts } from 'expo-font';
import * as SplashScreen from 'expo-splash-screen';
import { StatusBar } from 'expo-status-bar';
import { useState} from 'react';
import 'react-native-reanimated';

import {StyleSheet, TextInput, View, TouchableOpacity, Button} from 'react-native';

import { useColorScheme } from '@/hooks/useColorScheme';
import { ThemedText } from '@/components/ThemedText';
import { router } from 'expo-router';

import { emailValidator, passwordValidator } from '../utils';


// Prevent the splash screen from auto-hiding before asset loading is complete.
SplashScreen.preventAutoHideAsync();

export default function LoginScreen() {
  const [password, setPassword] = useState({ value: '', error: '' });
  const [email, setEmail] = useState({ value: '', error: '' });



  // TODO : Это пиздец, мои чуваки. Нужно поменять локал сторэдж на что-то вменяемое
  const _onLoginPressed = () => {
    const emailError = emailValidator(email.value);
    const passwordError = passwordValidator(password.value);

    // if (emailError || passwordError) {
    //   setEmail({ ...email, error: emailError });
    //   setPassword({ ...password, error: passwordError });
    //   return;
    // }

    const formData = new FormData();
    formData.append('username', email.value);
    formData.append('password', password.value);


    
   
    // router.navigate('/(tabs)');
    console.log("try to fetch",  email.value, password.value)
    fetch('http://127.0.0.1:8000/auth/token', {
      method: 'POST',
      body: formData,
      mode: "cors",
    }).then((res) => {
      console.log('auth res:', res);
      if (res.ok) {
        res.json().then((data) => {
          console.log("next step must be redirection", data);
          localStorage.setItem("access_token", data["access_token"])
          router.navigate('/(tabs)/allTasks');
          // router.replace('/');
          // navigation &&
          //   navigation.navigate('Dashboard', { token: data.access_token });
        });
      }
    });
  };


  const colorScheme = useColorScheme();
  const [loaded] = useFonts({
    SpaceMono: require('../../assets/fonts/SpaceMono-Regular.ttf'),
  });

  // useEffect(() => {
  //   if (loaded) {
  //     SplashScreen.hideAsync();
  //   }
  // }, [loaded]);

  // if (!loaded) {
  //   return null;
  // }

  return (
    <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
      <ThemedText> login (needs normal stylesheet) </ThemedText>
      {/* <ThemedText> looking throught email : {email.value} </ThemedText> */}
        <TextInput
          style={styles.input}
          returnKeyType="next"
          // value={email.value}
          onChangeText={(text) => {setEmail({ value: text, error: '' }); console.log(email)} }
          // error={!!email.error}
          // errorText={email.error}
          autoCapitalize="none"
          // autoCompleteType="email"
        />

        <TextInput
          style={styles.input}

          // label="Password"
          returnKeyType="done"
          // value={password.value}
          onChangeText={(text) => {setPassword({ value: text, error: '' }); console.log(email)}}
          // error={!!password.error}
          // errorText={password.error}
          secureTextEntry
        />

        

        <Button title="Login" onPress={_onLoginPressed} />
      <StatusBar style="auto" />
    </ThemeProvider>
  );
}

const styles = StyleSheet.create({
  input: {
    height: 40,
    margin: 12,
    borderWidth: 1,
    padding: 10,
  },
});
