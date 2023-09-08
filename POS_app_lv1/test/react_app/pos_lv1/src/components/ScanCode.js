import React, { useState, useEffect } from 'react';
import Quagga from 'quagga';


const ScanCode = (props) => {
  const [barcode, setBarcode] = useState('');

  useEffect(() => {
    Quagga.onDetected((result) => {
      if (result !== undefined) {
        setBarcode(result.codeResult.code);
        // バーコードがスキャンされたら、親コンポーネントにバーコードを渡す
        props.onBarcodeScanned(result.codeResult.code);
      }
    });
    const config = {
      inputStream: {
        name: 'Live',
        type: 'LiveStream',
        target: '#preview',
        constraints: {
            width: 300,
            height: 100,
            facingMode: 'environment',
        },
        singleChannel: false,
      },
      locator: {
        patchSize: 'medium',
        halfSample: true,
      },
      decoder: {
        readers: [
          {
            format: 'code_128_reader',
            config: {},
          },
        ],
      },
      numOfWorker: navigator.hardwareConcurrency || 4,
      locate: true,
      src: null,
    };

    Quagga.init(config, function (err) {
      if (err) {
        console.log(err);
        return;
      }
      Quagga.start();
    });
  }, [props]);

  return (
    <div>
      <h5>バーコードスキャナ</h5>
      <hr />
      <div>{barcode !== '' ? `バーコード：${barcode}` : 'スキャン中'}</div>
      <div id="preview"></div>
      <hr />
    </div>
  );
};

export default ScanCode;
