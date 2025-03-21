export  function emailValidator (email: string){
    const re = /\S+@\S+\.\S+/;
  
    if (!email || email.length <= 0) return 'Email cannot be empty.';
    if (!re.test(email)) return 'Ooops! We need a valid email address.';
  
    return '';
  };
  
  export  function passwordValidator (password: string) {
    if (!password || password.length <= 0) return 'Password cannot be empty.';
  
    return '';
  };
  
  export  function nameValidator (name: string) {
    if (!name || name.length <= 0) return 'Name cannot be empty.';
  
    return '';
  };
  