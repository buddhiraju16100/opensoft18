import React, { Component } from 'react';
import { post } from 'axios';

class SimpleReactFileUpload extends Component {
  constructor(props) {
    super(props);
    this.state = {
      file: null,
    };
    this.onFormSubmit = this.onFormSubmit.bind(this);
    this.onChange = this.onChange.bind(this);
    this.fileUpload = this.fileUpload.bind(this);
  }

  onFormSubmit(e) {
    e.preventDefault(); // Stop form submit
    this.fileUpload(this.state.file).then((response) => {
      console.log(response.data);
    });
  }

  onChange(e) {
    this.setState({ file: e.target.files[0] });
  }

  fileUpload(fileToUpload) {
    const url = 'http://localhost:8080/upload';
    const formData = new FormData();
    formData.append('file', fileToUpload);
    const config = {
        headers: {
            'content-type': 'multipart/form-data',
        },
    };
    return post(url, formData, config)
  }

  render() {
    const headerStyle = {
      fontSize: 35,
      color: 'yellow',
    };
    return (
      <form onSubmit={this.onFormSubmit}>
        <h1 style={headerStyle}>
          Upload the image that you want to analyze
        </h1>
        <input type="file" onChange={this.onChange} />
        <button type="submit">Upload</button>
      </form>
    );
  }
}

export default SimpleReactFileUpload;