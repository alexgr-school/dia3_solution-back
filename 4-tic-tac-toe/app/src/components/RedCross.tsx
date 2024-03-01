import React from 'react';

const RedCross = () => {
    return (
        <>
            <div className="h-8 w-1 bg-red-500 absolute transform -rotate-45 rounded"></div>
            <div className="h-8 w-1 bg-red-500 absolute transform rotate-45 rounded"></div>
        </>
    );
};

export default RedCross;
