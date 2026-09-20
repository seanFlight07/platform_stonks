interface HeaderProps {
  title: string
  subtitle: string
}


function Header(props: HeaderProps){
  return(
    <header>
      <h1>{props.title}</h1>
      <p>{props.subtitle}</p>
    </header>
  )
}
export  default Header
