import './App.scss';
import {MenuItem, Select, Tooltip} from "@material-ui/core";
import {MuiPickersUtilsProvider} from '@material-ui/pickers';
import DateFnsUtils from '@date-io/date-fns';
import {DatePicker} from "@material-ui/pickers";
import {useEffect, useState} from "react";
import {BarChart, Bar, CartesianGrid, Legend, ResponsiveContainer, XAxis, YAxis} from "recharts";

function App() {

  const codes = {
    'MOW': "Moscow",
    'LED': "Saint Petersburg",
    'KZN': "Kazan",
    'CEK': "Chelyabinsk",
    'SVX': "Ekaterinburg",
    'AER': "Sochi",
    'KRR': "Krasnodar",
    'KGD': "Kaliningrad",
    'SGC': "Surgut",
    'OVB': "Novosibirsk",
    'VVO': "Vladivostok",
    'YKS': "Yakutsk"
  }

  const codeKeys = Object.keys(codes)

  const [origin, setOrigin] = useState(codeKeys[0])
  const [destination, setDestination] = useState(codeKeys[1])
  const [departureDate, setDepartureDate] = useState(new Date())

  const onSetDestination = (event) => {
    setDestination(event.target.value)
  }

  const onSetOrigin = (event) => {
    setOrigin(event.target.value)
  }

  const onSetDepartureDate = (date) => {
    setDepartureDate(date)
  }

  const [data, setData] = useState([])

  useEffect(()=>{
    getGraphData()
  }, [departureDate, origin, destination])

  const getGraphData = () => {
    const today = new Date()
    today.setDate(today.getDate()-3)
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", "http://127.0.0.1:5000/predict_prices", true);
    xmlHttp.setRequestHeader("Access-Control-Allow-Origin", "*")
    xmlHttp.setRequestHeader("Content-type", "application/json")
    xmlHttp.send(JSON.stringify({
      "origin" : origin,
      "destination": destination,
      "date": `${today.getDate()}.${today.getMonth()}.${today.getFullYear().toString().slice(2,)}`,
      "flight_date": `${departureDate.getDate()}.${departureDate.getMonth()}.${departureDate.getFullYear().toString().slice(2,)}`,
    }));

    xmlHttp.onerror = () =>{
    }

    xmlHttp.onload = () => {
      let responseData = JSON.parse(xmlHttp.response)
      let newData = []

      let days = responseData.days.reverse()
      let predictions = responseData.prices.reverse()
      let real = responseData.real_prices.reverse()

      for (let i = 0; i < days.length; i++) {
        newData.push({
          name: days[i],
          prediction: predictions[i],
          realPrices: i < real.length ? real[i]: 0,
        },)
      }

      console.log(newData)
      setData(newData)
    }
  }

  return (
    <div className="App">
      <div className={"main-wrapper"}>
        <div className={"selects"}>
          <Select
            className={"select"}
            variant="outlined"
            value={origin}
            onChange={onSetOrigin}
          >
            {codeKeys.map(key => {
              return <MenuItem value={key}>{codes[key]}</MenuItem>
            })}
          </Select>

          <span className={"pointer"}>
          →
        </span>
          <Select
            className={"select"}
            variant="outlined"
            value={destination}
            onChange={onSetDestination}
          >
            {codeKeys.map(key => {
              return <MenuItem value={key}>{codes[key]}</MenuItem>
            })}
          </Select>
        </div>

        <MuiPickersUtilsProvider utils={DateFnsUtils}>
          <DatePicker
            className={"date-picker"}
            autoOk
            orientation="landscape"
            variant="static"
            openTo="date"
            value={departureDate}
            onChange={onSetDepartureDate}
          />
        </MuiPickersUtilsProvider>

        <div className={"chart"}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              width={500}
              height={300}
              data={data}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3"/>
              <XAxis dataKey="name"/>
              <YAxis/>
              <Tooltip/>
              <Legend/>
              <Bar dataKey="prediction" fill="#8896E3"/>
              <Bar dataKey="realPrices" fill="#3f51b5"/>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

export default App;
