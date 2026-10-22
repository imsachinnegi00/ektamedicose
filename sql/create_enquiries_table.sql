-- Run this once in SQL Server Management Studio against EnquiryDB.
CREATE TABLE dbo.Enquiries (
    EnquiryID INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    FullName NVARCHAR(120) NOT NULL,
    BusinessName NVARCHAR(160) NOT NULL,
    Mobile NVARCHAR(20) NOT NULL,
    Email NVARCHAR(254) NULL,
    City NVARCHAR(100) NOT NULL,
    State NVARCHAR(100) NOT NULL,
    EnquiryType NVARCHAR(80) NOT NULL,
    Category NVARCHAR(120) NULL,
    Message NVARCHAR(2000) NULL,
    Consent BIT NOT NULL,
    Status NVARCHAR(30) NOT NULL CONSTRAINT DF_Enquiries_Status DEFAULT N'New',
    CreatedAt DATETIME2 NOT NULL CONSTRAINT DF_Enquiries_CreatedAt DEFAULT SYSDATETIME()
);
