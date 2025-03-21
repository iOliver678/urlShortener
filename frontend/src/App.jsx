import { useEffect, useState} from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const[dataList, setDataList] = useState([])
  const[url, setUrl] = useState('')
  const [alias, setAlias] = useState('')
  const host_url = import.meta.env.VITE_BACKEND_URL;

  
  
  function isValidUrl(string) {
    try {
      console.log(new URL(string));
      return true;
    } catch (err) {
      return false;
    }
  }
  class ValidationError extends Error {
    constructor(message) {
      super(message);
      this.name = "ValidationError";
    }
  }
  const handleDelete = async (aliasToDelete) => {
    try {
      const response = await fetch(`${host_url}/delete/${aliasToDelete}`, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error(`Failed to delete alias: ${aliasToDelete}`);
      }

      // Filter out the deleted item from the dataList state
      setDataList(dataList.filter((item) => item.alias !== aliasToDelete));
      alert('Entry  successfully deleted');
    } catch (error) {
      console.error('Error deleting entry:', error);
      alert('Could not delete the entry. Please try again.');
    }
  };

  const handleUpload = async (e) => {
    
    e.preventDefault();
    
    const data = {
      url: url,
    };
    
   
    if(alias.length>0){
      data.alias = alias
    }
    
    try{
      if (!isValidUrl(url)){
        throw new ValidationError(`Invalid Url!`)
      }
      const response = await fetch(`${host_url}/upload`,{
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      });
    
      
      if(!response.ok){
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      console.log(result);
      data.alias = result.alias
      data.link = `${host_url}/search/${data.alias}`
      setDataList([...dataList,data]);
    }
    catch (error) {
      if (error instanceof ValidationError){
        alert("URL is invalid")
        return;
      }
      else{
      console.error('Error uploading data:',error)
      alert(`Alias is taken, try again`)
      }
    }

    setUrl('');
    setAlias('');
  };
  
  useEffect(() => {
    // first page load

    const fetchData = async () => {
      try{
      const response = await fetch(`${host_url}/all`)
      console.log(response)
      const result = await response.json();

      if(result && Array.isArray(result)){
      const updatedData = result.map(item => ({
          ...item,
          link: `${host_url}/search/${item.alias}`
      }));
      setDataList(updatedData);
    }else {
      setDataList([])
    }
    }
    catch (error){
      
      console.error('Error fetching data:', error);
      
    }
    };
    fetchData();
    
  }, []);

 return(
  <div id="body">
    <header id="title">Create a new link</header>
    <form onSubmit={handleUpload}>

    <div className='inputBoxes'>
    <input
      type="text"
      id="urlFromUser"
      placeholder='Enter URl - https://'
      value={url}
      onChange={(e) => setUrl(e.target.value)}
      />
    <input
      type="text"
      id="aliasFromUser"
      placeholder='Alias'
      value={alias}
      onChange={(e) => setAlias(e.target.value)}
      />
    <button id="createUrl" type="submit"> Create</button>
    </div>
    </form>
    <p id="tableHeader">List of URL's:</p>
    <table className='urlTable'>
    <thead>
      <tr className="header-panel">
        <th id="url-table">Url</th>
        <th>Alias</th>
        <th>Link</th>
        <th id='trashCan'></th>
      </tr>
    </thead>
    <tbody>
      {dataList.map((data, index) => (
        <tr key={index}>
          <td id="url-display">{data.url}</td>
          <td id="alias-display">{data.alias}</td>
          <td> <a id="link-display" href={data.link} target='_blank'>{data.link}</a></td>
          <td id="delete"><button onClick={() => handleDelete(data.alias)}>delete</button></td>
        </tr>
      ))}
    </tbody>
    </table>
  </div>
 );
}

export default App
