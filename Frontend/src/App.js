import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Container, Form, Button, Alert, Card } from 'react-bootstrap';
import './App.css';

function App() {
  const [pnrNumber, setPnrNumber] = useState('');
  const [pnrStatus, setPnrStatus] = useState(null);
  const [error, setError] = useState('');

  const getPnrStatusButtonRef = useRef(null);

  useEffect(() => {
    if (pnrStatus) {
      console.log(pnrStatus); // Log PNR status whenever it's updated
    }
  }, [pnrStatus]);

  const handleGetPnrStatus = async () => {
    try {
      const response = await axios.get(`https://decaptcha-pnr-backend.onrender.com/finpredict?pnrnumber=${pnrNumber}`);
      setPnrStatus(response.data);
      setError('');
    } catch (error) {
      setPnrStatus(null);
      setError('Failed to fetch PNR status. Please check the PNR number.');
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      getPnrStatusButtonRef.current.click();
    }
  };

  return (
    <Container className="mt-5">
      <h1>Indian Railways PNR Status</h1>

      <Form className="my-3">
        <Form.Group controlId="pnrNumber" className="form-group">
          <Form.Label className="form-label">Enter PNR Number:</Form.Label>
          <Form.Control
            type="text"
            value={pnrNumber}
            onChange={(e) => setPnrNumber(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Enter your PNR number here"
          />
        </Form.Group>

        <Button
          ref={getPnrStatusButtonRef}
          variant="primary"
          onClick={handleGetPnrStatus}
          className="mt-3"
        >
          Get PNR Status
        </Button>
      </Form>

      {error && <Alert variant="danger" className="mt-3">{error}</Alert>}

      {pnrStatus && pnrStatus.errorMessage && (
        <Alert variant="warning" className="mt-3">
          FLUSHED PNR / PNR not generated yet.
        </Alert>
      )}

      {pnrStatus && pnrStatus.arrivalDate && (
        <Card className="mt-3 pnr-card">
          <Card.Body>
            <div className="train-info">
              <h4>{pnrStatus.trainName} ({pnrStatus.trainNumber})</h4>
              <p><strong>From:</strong> {pnrStatus.boardingPoint} <strong>To:</strong> {pnrStatus.destinationStation}</p>
              <p><strong>Departure:</strong> {pnrStatus.dateOfJourney}</p>
            </div>

            <div className="pnr-info">
              <p><strong>PNR:</strong> {pnrStatus.pnrNumber} <strong>Class:</strong> {pnrStatus.journeyClass} <strong>Quota:</strong> {pnrStatus.quota}</p>
            </div>

            <div className="passenger-info">
              {pnrStatus.passengerList.map((passenger, index) => (
                <div key={index} className="passenger-status">
                  <p><strong>Passenger {index + 1}:</strong></p>
                  <p><strong>Booking Status:</strong> {passenger.bookingStatusDetails}</p>
                  <p><strong>Current Status:</strong> {passenger.currentStatusDetails}</p>
                  <p><strong>Coach Position:</strong> {passenger.bookingCoachId}</p>
                </div>
              ))}
            </div>


          </Card.Body>
        </Card>
      )}
    </Container>
  );
}

export default App;


























// // import React, { useState, useRef } from 'react';
// // import axios from 'axios';
// // import { Container, Form, Button, Table } from 'react-bootstrap';
// // import './App.css';
// // function App() {
// //   const [pnrNumber, setPnrNumber] = useState('');
// //   const [pnrStatus, setPnrStatus] = useState(null);
// //   const [error, setError] = useState('');

// //   const handleGetPnrStatus = async () => {
// //     try {
// //       const response = await axios.get(`https://decaptcha-pnr-backend.onrender.com/finpredict?pnrnumber=${pnrNumber}`);
// //       setPnrStatus(response.data);
// //       setError('');
// //       console.log(pnrStatus)
// //     } catch (error) {
// //       setPnrStatus(null);
// //       setError('Failed to fetch PNR status. Please check the PNR number.');
// //     }
// //   };
// //   const handleKeyPress = (event) => {
// //     if (event.key === 'Enter') {
// //       event.preventDefault(); // Prevent form submission
// //       getPnrStatusButtonRef.current.click(); // Trigger button click event
// //     }
// //   };
// //   const getPnrStatusButtonRef = useRef(null);
// //   return (
// //     <Container className="mt-5">
// //       <h1>Indian Railways PNR Status</h1>
// //       <Form className="my-3">
// //         <Form.Group controlId="pnrNumber">
// //           <Form.Label>Enter PNR Number:</Form.Label>
// //           <Form.Control
// //             type="text"
// //             value={pnrNumber}
// //             onChange={(e) => setPnrNumber(e.target.value)}
// //             onKeyDown={handleKeyPress}
// //           />
// //         </Form.Group>
// //         <Button ref={getPnrStatusButtonRef}
// //           variant="primary"
// //           onClick={handleGetPnrStatus}>
// //           Get PNR Status
// //         </Button>
// //       </Form>

// //       {pnrStatus && pnrStatus.errorMessage && <p className="text-danger">{"FLUSHED PNR/PNR not generated yet"}</p>}
// //       {pnrStatus && pnrStatus.arrivalDate && (

// //         <Table striped bordered hover className="mt-3">
// //           <thead>
// //             <tr>
// //               <th>Serial No</th>
// //               <th>Booking Berth Code</th>
// //               <th>Booking Berth No</th>
// //               <th>Booking Coach Id</th>
// //               <th>Booking Status</th>
// //             </tr>
// //           </thead>
// //           <tbody>
// //             {pnrStatus.passengerList.map((passenger, index) => (
// //               <tr key={index}>
// //                 <td>{index + 1}</td>
// //                 <td>{passenger.bookingBerthCode}</td>
// //                 <td>{passenger.bookingBerthNo}</td>
// //                 <td>{passenger.bookingCoachId}</td>
// //                 <td>{passenger.bookingStatus}</td>
// //               </tr>
// //             ))}
// //           </tbody>
// //         </Table>
// //       )}
// //     </Container>
// //   );
// // }
// // export default App;