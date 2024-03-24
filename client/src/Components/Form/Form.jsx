import React, { useState } from 'react';
import axios from 'axios';
import './Form.scss';
import ClipLoader from "react-spinners/ClipLoader";

const Form = () => {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState('');
    const [freq, setFreq] = useState();
    const [loader,setLoader] = useState(false);
    const handleChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setResult('');
        if (!file || !file.type.startsWith('image')) {
            alert('Please upload an image file.');
            return;
        }
        setLoader(true);
        const formData = new FormData();
        formData.append('files[]', file);
        formData.append('filename', file.name);

        try {
            const response = await axios.post("http://localhost:5001/upload", formData);
            setResult(response.data.annotated_image_url);
            let input_data = response.data.count;
            setFreq(Object.entries(input_data).map(([key, value]) => ({ key, value })));
            console.log(response);
            setLoader(false);
            document.getElementById('images').scrollIntoView({ behavior: 'smooth' });
        } catch (error) {
            console.error("Error uploading file:", error);
            alert("Some error occurred please try again");
        }
    };

    return (
        <div className='form_and_result'>
            <section className='form' id='form'>
                <h1>Upload Image</h1>
                <form onSubmit={handleSubmit}>
                    <input type='file' onChange={handleChange} />
                    <button type='submit'>Submit</button>
                </form>
                {loader && <span className='spinner'><ClipLoader color='white'/></span>}
            </section>
            <section className='images' id='images'>
                {file === null ? <h1>Please upload an image ...</h1> :
                    <div className='orig'>
                        <h1>Uploaded Image</h1>
                        <img src={URL.createObjectURL(file)} alt='Please upload image' />
                    </div>
                }
                <div className='result'>
                    {(file !== null && result === '') ? <h1>Please press the submit button</h1> : result &&
                        <div className='result'>
                            <h1>Result</h1>
                            <img src={result} alt='/' />
                        </div>
                    }
                </div>
            </section>
            {
                result && 
                <section className='result_content' id='result_content'>
                <h1>Objects detected</h1>
                <ul className='freq'>
                    {freq && freq.map((item,index)=>
                        <li key={index}>
                            <span className='item'>{item.key}</span>
                            <span className='value'>{item.value}</span>
                        </li>
                    )}
                    
                </ul>
                </section>
            }
        </div>
    );
};

export default Form;
